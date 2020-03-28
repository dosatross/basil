from datetime import datetime as dt
from django.db.models import Q, Func, F
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
from basil.apps.transactions.api.utils import filter_category_set, filter_transactions, parse_date_range

class TransactionsViewSet(viewsets.ModelViewSet):
  serializer_class = TransactionSerializer
  permission_classes = (permissions.IsAuthenticated,)
  filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
  filter_fields = ('category__groups__name','category__subcategory','category__name', 'category__is_internal', 'category__is_credit', 'category__is_adjustment')
  search_fields = ('description','category__name','category__subcategory','category__groups__name')
  ordering_fields = ('amount', 'date')

  def get_queryset(self):
    user = self.request.user
    queryset = Transaction.objects.filter(user=user)
    qp = self.request.query_params
    return filter_transactions(queryset,qp.get('date_range'),qp.get('top'))

class IncomeViewSet(TransactionsViewSet):

  def get_queryset(self):
    user = self.request.user
    queryset = Transaction.objects.filter(Q(category__in=Category.get_income_categories()) & Q(user=user))
    qp = self.request.query_params
    return filter_transactions(queryset,qp.get('date_range'),qp.get('top'))

class ExpensesViewSet(TransactionsViewSet):

  def get_queryset(self):
    user = self.request.user
    queryset = Transaction.objects.filter(Q(category__in=Category.get_expense_categories()) & Q(user=user))
    qp = self.request.query_params
    return filter_transactions(queryset,qp.get('date_range'),qp.get('top'))

class PeriodTotalView(APIView):
  permission_classes = (permissions.IsAuthenticated,)

  def get(self, request, set, period_len):
    if period_len not in PERIOD_LENGTHS:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    qp = request.query_params
    category_set =  filter_category_set(set,qp.get('group'),qp.get('include'),qp.get('exclude'))
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
      date_range = date_start_end(request.user)
    
    qp = request.query_params
    category_set =  filter_category_set(set,qp.get('group'),qp.get('include'),qp.get('exclude'))
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

    qp = request.query_params
    category_set =  filter_category_set(set,qp.get('group'),qp.get('include'),qp.get('exclude'))
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

    qp = request.query_params
    category_set =  filter_category_set(set,qp.get('group'),qp.get('include'),qp.get('exclude'))
    if not category_set:
      return Response(status=status.HTTP_400_BAD_REQUEST)

    q = Transaction.category_period_total(
      request.user,
      period_len,
      category_set)
    serializer = CategoryPeriodTotalTransactionSerializer(q, many=True)
    return Response(serializer.data)

class DateRange(APIView):
  permission_classes = (permissions.IsAuthenticated,)

  def get(self, request):
    return Response(date_start_end(request.user))