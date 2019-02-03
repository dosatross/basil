import datetime
from django.db.models import Q
from django.db.models.functions import TruncWeek, TruncMonth, TruncQuarter, TruncYear
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from basil.apps.transactions.models import Transaction
from basil.apps.transactions.api.serializers import (TransactionSerializer, PeriodTotalTransactionSerializer, 
											CategoryTotalTransactionSerializer, PeriodCategoryTotalTransactionSerializer,
											CategoryPeriodTotalTransactionSerializer)
from basil.apps.categories.models import Category, CategoryGroup


class TransactionsViewSet(viewsets.ModelViewSet):
	serializer_class = TransactionSerializer
	permission_classes = (permissions.IsAuthenticated,)
	filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
	filter_fields = ('category__groups__name','category__subcategory','category__name', 'category__is_internal', 'category__is_credit', 'category__is_adjustment')
	search_fields = ('description','category__name','category__subcategory','category__groups__name')
	ordering_fields = ('amount', 'date')

	def get_queryset(self):
		user = self.request.user
		return Transaction.objects.filter(user=user)

class IncomeViewSet(TransactionsViewSet):

	def get_queryset(self):
		user = self.request.user
		return Transaction.objects.filter(Q(category__in=Category.get_income_categories()) & Q(user=user))

class ExpensesViewSet(TransactionsViewSet):

	def get_queryset(self):
		user = self.request.user
		return Transaction.objects.filter(Q(category__in=Category.get_expense_categories()) & Q(user=user))

class PeriodTotalView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	valid = ['w','m','q','y']

	def get(self, request, set, period):
		if period not in PeriodTotalView.valid:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		category_set =  parse_set_query_param(set,request)
		if not category_set:
			Response(status=status.HTTP_400_BAD_REQUEST)

		q = Transaction.period_total(
			request.user,
			get_trunc(period),
			category_set)
		serializer = PeriodTotalTransactionSerializer(q, many=True)
		return Response(serializer.data)

class CategoryTotalView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, set):
		category_set =  parse_set_query_param(set,request)
		if not category_set:
			Response(status=status.HTTP_400_BAD_REQUEST)

		q = Transaction.category_total(
			request.user,
			category_set)
		serializer = CategoryTotalTransactionSerializer(q, many=True)
		return Response(serializer.data)

class PeriodCategoryTotalView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, set, period):
		if period not in PeriodTotalView.valid:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		category_set =  parse_set_query_param(set,request)
		if not category_set:
			Response(status=status.HTTP_400_BAD_REQUEST)

		q = Transaction.period_category_total(
			request.user,
			get_trunc(period),
			category_set)
		serializer = PeriodCategoryTotalTransactionSerializer(q, many=True)
		return Response(serializer.data)

class CategoryPeriodTotalView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, set, period):
		if period not in PeriodTotalView.valid:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		category_set =  parse_set_query_param(set,request)
		if not category_set:
			Response(status=status.HTTP_400_BAD_REQUEST)

		q = Transaction.category_period_total(
			request.user,
			get_trunc(period),
			category_set)
		serializer = CategoryPeriodTotalTransactionSerializer(q, many=True)
		return Response(serializer.data)

def get_trunc(period):
	if period == 'w': trunc = TruncWeek
	if period == 'm': trunc = TruncMonth
	if period == 'q': trunc = TruncQuarter
	if period == 'y': trunc = TruncYear
	return trunc

def parse_set_query_param(set,request):
	if set == 'income':
		category_set = Category.get_income_categories()
	elif set == 'expenses':
		category_set = Category.get_expense_categories()
	elif set == 'group':
		group_name = request.query_params.get('group')
		if not group_name or not CategoryGroup.objects.filter(name=group_name).first():
			return None
		else:
			category_set = CategoryGroup.objects.filter(name=group_name).first().categories.all()
	else:
		return None
	return category_set