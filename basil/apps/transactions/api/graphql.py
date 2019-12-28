from django.db.models import Q
from graphql import GraphQLError
import graphene
from graphene import ObjectType, Field, String, Date, Float, Int, List, ID
from graphene_django.types import DjangoObjectType
from graphene.types.resolver import dict_resolver

from basil.apps.transactions.models import Transaction
from basil.apps.transactions.utils import date_start_end
from basil.apps.transactions.constants import ISO_DATE_FORMAT, PERIOD_WEEK, PERIOD_MONTH, PERIOD_QUARTER,PERIOD_YEAR, PERIOD_LENGTHS
from basil.apps.transactions.api.utils import filter_category_set, parse_date_range, filter_transactions
from basil.apps.categories.models import Category
from basil.apps.categories.api.graphql import CategoryType

class TransactionType(DjangoObjectType):
  class Meta:
    model = Transaction

class TransactionQuery(ObjectType):
  transaction = Field(TransactionType,id=ID(required=True))
  all_transactions = List(TransactionType,date_range=String(),top=Int())
  income = List(TransactionType,date_range=String(),top=Int())
  expenses = List(TransactionType,date_range=String(),top=Int())

  def resolve_transaction(self, info, id):
    return Transaction.objects.get(id=id)

  def resolve_all_transactions(self, info, date_range=None, top=None):
    qs = Transaction.objects.filter(user=info.context.user)
    return filter_transactions(qs,date_range,top)

  def resolve_income(self, info, date_range=None, top=None):
    user=info.context.user
    qs = Transaction.objects.filter(Q(category__in=Category.get_income_categories()) & Q(user=user))
    return filter_transactions(qs,date_range,top)

  def resolve_expenses(self, info, date_range=None, top=None):
    user=info.context.user
    qs = Transaction.objects.filter(Q(category__in=Category.get_expense_categories()) & Q(user=user))
    return filter_transactions(qs,date_range,top)
    

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
    exclude = String())

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
  periods_starting = List(PeriodTotalType)
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