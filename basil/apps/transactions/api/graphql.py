from django.db.models import Q
from django.db.models.query import QuerySet
from graphql import GraphQLError
import graphene
from graphene import ObjectType, Field, String, Date, Float, Int, List, ID, Enum, relay
from graphene_django_extras import DjangoSerializerMutation, DjangoInputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from basil.utils.graphql import Connection
from basil.apps.transactions.models import Transaction
from basil.apps.transactions.filters import TransactionFilter
from basil.apps.transactions.api.serializers import TransactionSerializer
from basil.apps.transactions.utils import date_start_end
from basil.apps.transactions.constants import ISO_DATE_FORMAT, PERIOD_WEEK, PERIOD_MONTH, PERIOD_QUARTER,PERIOD_YEAR, PERIOD_LENGTHS
from basil.apps.transactions.api.utils import filter_category_set, parse_date_range, filter_transactions
from basil.apps.categories.models import Category
from basil.apps.categories.api.graphql import CategoryType, CategoryGroupType


class TransactionType(DjangoObjectType):
  class Meta:
    model = Transaction
    interfaces = (relay.Node, )
    connection_class = Connection
  
  @classmethod
  def get_node(cls, info, id):
    return Transaction.objects.get(id=id)

class TransactionQuery(ObjectType):
  transaction_connection = DjangoFilterConnectionField(TransactionType, filterset_class=TransactionFilter, enforce_first_or_last=True)
  income_connection = DjangoFilterConnectionField(TransactionType, filterset_class=TransactionFilter, enforce_first_or_last=True)
  expenses_connection = DjangoFilterConnectionField(TransactionType, filterset_class=TransactionFilter, enforce_first_or_last=True)

  def resolve_transaction_connection(self, info, **kwargs):
    return Transaction.objects.filter(user=info.context.user).select_related('category')

  def resolve_income(self, info):
    user=info.context.user
    return Transaction.objects.filter(Q(category__in=Category.get_income_categories()) & Q(user=user))

  def resolve_expenses(self, info):
    user=info.context.user
    return Transaction.objects.filter(Q(category__in=Category.get_expense_categories()) & Q(user=user))

class TransactionMutation(DjangoSerializerMutation):

  @classmethod
  def get_serializer_kwargs(cls, root, info, **kwargs):
    return {'context': {'request': info.context}}

  class Meta:
    serializer_class = TransactionSerializer
    exclude_fields = ('user', )
    input_field_name = 'input'

class DateRangeType(ObjectType):
  start = Date()
  end = Date()

class DateRangeQuery(ObjectType):
  date_range = Field(DateRangeType)

  def resolve_date_range(self, info, **kwargs):
    return date_start_end(info.context.user)


class PeriodTotalType(ObjectType):
  total = Float()
  period_starting = Date()

class PeriodTotalQuery(ObjectType):
  period_total = List(PeriodTotalType,
    period_len = String(required=True),
    set = String(required=True),
    group_name = String(),
    include = String(),
    exclude = String()
  )

  def resolve_period_total(self, info, period_len, set, group_name=None, include=None, exclude=None):
    if period_len not in PERIOD_LENGTHS:
      raise GraphQLError()
    category_set =  filter_category_set(set,group_name, include, exclude)
    if not category_set:
      raise GraphQLError()
    return Transaction.period_total(
      info.context.user,
      period_len,
      category_set)


class CategoryTotalType(graphene.ObjectType):
  total = Float()
  category = Field(CategoryType)

class CategoryTotalQuery(ObjectType):
  category_total = List(CategoryTotalType,
    set = String(required=True),
    top = Int(),
    date_range = String(),
    group_name = String(),
    include = String(),
    exclude = String())

  def resolve_category_total(self, info, set, top=None, date_range=None, group_name=None, include=None, exclude=None):
    if date_range:
      date_range = parse_date_range(date_range)
      if not date_range:
        raise GraphQLError()
    else:
      date_range = date_start_end(info.context.user)

    category_set =  filter_category_set(set,group_name, include, exclude)
    if not category_set:
      raise GraphQLError()

    return Transaction.category_total(
      info.context.user,
      category_set,
      date_range,
      top)

class PeriodCategoryTotalType(ObjectType):
  categories = List(CategoryTotalType)
  period_starting = Date()

class PeriodCategoryTotalQuery(ObjectType):
  period_category_total = List(PeriodCategoryTotalType,
    period_len = String(required=True),
    set = String(required=True),
    group_name = String(),
    include = String(),
    exclude = String())

  def resolve_period_category_total(self, info, period_len, set, group_name=None, include=None, exclude=None):
    if period_len not in PERIOD_LENGTHS:
      raise GraphQLError()
    category_set =  filter_category_set(set,group_name, include, exclude)
    if not category_set:
      raise GraphQLError()
    return Transaction.period_category_total(
      info.context.user,
      period_len,
      category_set)


class CategoryPeriodTotalType(ObjectType):
  period_totals = List(PeriodTotalType)
  category = Field(CategoryType)

class CategoryPeriodTotalQuery(ObjectType):
  category_period_total = List(CategoryPeriodTotalType,
    period_len = String(required=True),
    set = String(required=True),
    group_name = String(),
    include = String(),
    exclude = String())

  def resolve_category_period_total(self, info, period_len, set, group_name=None, include=None, exclude=None):
    if period_len not in PERIOD_LENGTHS:
      raise GraphQLError()
    category_set =  filter_category_set(set,group_name, include, exclude)
    if not category_set:
      raise GraphQLError()
    return Transaction.category_period_total(
      info.context.user,
      period_len,
      category_set)

class CategorySet(Enum):
    income = 'income'
    expenses = 'expenses'
    group = 'group'

class CategorySetPeriodTotalType(ObjectType):
  period_totals = List(PeriodTotalType)
  set = CategorySet()
  group = Field(CategoryGroupType)

class CategorySetPeriodTotalQuery(ObjectType):
  category_set_period_total = List(CategorySetPeriodTotalType,
    period_len = String(required=True))
  
  def resolve_category_set_period_total(self, info, period_len):
    if period_len not in PERIOD_LENGTHS:
      raise GraphQLError()
    return Transaction.category_set_period_total(info.context.user, period_len)
    
