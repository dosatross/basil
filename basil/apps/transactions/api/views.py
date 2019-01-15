import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from basil.apps.transactions.models import Transaction
from basil.apps.transactions.api.serializers import TransactionSerializer
from basil.apps.categories.models import Category


class TransactionsViewSet(viewsets.ModelViewSet):
	serializer_class = TransactionSerializer
	queryset = Transaction.objects.all()
	filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
	filter_fields = ('category__is_earned', 'category__is_credit')
	search_fields = ('description','category__name','category__subcategory')
	ordering_fields = ('amount', 'date')

class IncomeViewSet(TransactionsViewSet):
	queryset = Transaction.objects.filter(category__in=Category.get_income_categories())

class ExpensesViewSet(TransactionsViewSet):
	queryset = Transaction.objects.filter(category__in=Category.get_expense_categories())