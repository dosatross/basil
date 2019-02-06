from datetime import datetime as dt
from django.db.models import Q
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from basil.apps.transactions.models import Transaction
from basil.apps.transactions.utils import date_start_end
from basil.apps.transactions.constants import ISO_DATE_FORMAT, PERIOD_WEEK, PERIOD_MONTH, PERIOD_QUARTER,PERIOD_YEAR, PERIOD_LENGTHS
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

	def get(self, request, set, period_len):
		if period_len not in PERIOD_LENGTHS:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		category_set =  parse_set_query_param(set,request)
		if not category_set:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		q = Transaction.period_total(
			request.user,
			period_len,
			category_set)
		serializer = PeriodTotalTransactionSerializer(q, many=True)
		return Response(serializer.data)

class CategoryTotalView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, set):
		top_s = request.query_params.get('top')
		top = None
		if top_s and top_s.isdigit():
			top = int(top_s) 

		date_range_s = request.query_params.get('date_range')
		date_range = None
		if date_range_s:
			date_range = parse_date_range(date_range_s)
			if not date_range:
				return Response(status=status.HTTP_400_BAD_REQUEST)
		else:
			date_range = date_start_end()

		category_set =  parse_set_query_param(set,request)
		if not category_set:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		q = Transaction.category_total(
			request.user,
			category_set,
			date_range,
			top)
		serializer = CategoryTotalTransactionSerializer(q, many=True)
		return Response(serializer.data)

class PeriodCategoryTotalView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, set, period_len):
		if period_len not in PERIOD_LENGTHS:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		category_set =  parse_set_query_param(set,request)
		if not category_set:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		q = Transaction.period_category_total(
			request.user,
			period_len,
			category_set)
		serializer = PeriodCategoryTotalTransactionSerializer(q, many=True)
		return Response(serializer.data)

class CategoryPeriodTotalView(APIView):
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, set, period_len):
		if period_len not in PERIOD_LENGTHS:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		category_set =  parse_set_query_param(set,request)
		if not category_set:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		q = Transaction.category_period_total(
			request.user,
			period_len,
			category_set)
		serializer = CategoryPeriodTotalTransactionSerializer(q, many=True)
		return Response(serializer.data)



def parse_set_query_param(set,request):
	# get base category set
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
	elif set == 'transactions':
		category_set = Category.objects.all()
	else:
		return None

	include = request.query_params.get('include')
	if include:
		names = include.split(',')
		include_ids = []
		for name in names:
			group = CategoryGroup.objects.filter(name=name).first()
			if not group:
				return None
			include_ids += [c.id for c in group.categories.all()]
		base_ids = [c.id for c in category_set]
		include_ids += base_ids
		category_set = Category.objects.filter(id__in=include_ids) 

	exclude = request.query_params.get('exclude')
	if exclude:
		names = exclude.split(',')
		exclude_ids = []
		for name in names:
			group = CategoryGroup.objects.filter(name=name).first()
			if not group:
				return None
			exclude_ids += [c.id for c in group.categories.all()]
		category_set = category_set.exclude(id__in=exclude_ids)

	return category_set

def parse_date_range(date_range):
	str_arr = date_range.split(':')
	if len(str_arr) != 2:
		return None
	try :
		start = dt.strptime(str_arr[0],ISO_DATE_FORMAT).date()
		end = dt.strptime(str_arr[1],ISO_DATE_FORMAT).date()
	except ValueError:
		return None
	return {'start':start,'end':end}
