import datetime
from django.db.models.functions import TruncWeek, TruncMonth, TruncQuarter, TruncYear
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from basil.apps.transactions.models import Transaction
from basil.apps.transactions.api.serializers import TransactionSerializer, PeriodTransactionSerializer
from basil.apps.categories.models import Category


class TransactionsViewSet(viewsets.ModelViewSet):
	serializer_class = TransactionSerializer
	queryset = Transaction.objects.all()
	filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
	filter_fields = ('category__groups__name','category__subcategory','category__name', 'category__is_internal', 'category__is_credit', 'category__is_adjustment')
	search_fields = ('description','category__name','category__subcategory','category__groups__name')
	ordering_fields = ('amount', 'date')

class IncomeViewSet(TransactionsViewSet):
	queryset = Transaction.objects.filter(category__in=Category.get_income_categories())

class ExpensesViewSet(TransactionsViewSet):
	queryset = Transaction.objects.filter(category__in=Category.get_expense_categories())

class PeriodView(generics.ListAPIView):
	queryset = Transaction.objects.all()

	valid = ['w','m','q','y']

	@classmethod
	def get_trunc(cls,period):
		if period == 'w': trunc = TruncWeek
		if period == 'm': trunc = TruncMonth
		if period == 'q': trunc = TruncQuarter
		if period == 'y': trunc = TruncYear
		return trunc

class IncomePeriodView(PeriodView):

	def list(self, request, period):
		if period not in PeriodView.valid:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		q = Transaction.get_sum_over_period(
			PeriodView.get_trunc(period),
			Category.get_income_categories())
		serializer = PeriodTransactionSerializer(q, many=True)
		return Response(serializer.data)

class ExpensePeriodView(PeriodView):

	def list(self, request, period):
		if period not in PeriodView.valid:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		q = Transaction.get_sum_over_period(
			PeriodView.get_trunc(period),
			Category.get_expense_categories())
		serializer = PeriodTransactionSerializer(q, many=True)
		return Response(serializer.data)