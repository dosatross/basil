from django import forms
from django_filters import Filter, FilterSet, OrderingFilter, DateRangeFilter, NumberFilter
from django_filters.widgets import RangeWidget

from basil.apps.transactions.models import Transaction

class IntegerFilter(Filter):
  field_class = forms.IntegerField

class TransactionFilter(FilterSet):
  amount_top = IntegerFilter(method='filter_amount_top')
  amount_bottom = IntegerFilter(method='filter_amount_bottom')

  def filter_amount_top(self, queryset, name, value):
    return queryset.filter(category__is_internal=False).order_by('-amount')[:int(value)]

  def filter_amount_bottom(self, queryset, name, value):
    return queryset.filter(category__is_internal=False).order_by('amount')[:int(value)]

  class Meta:
    model = Transaction
    fields = {
        'description': ['icontains'],
        'amount': ['gte', 'lte'],
        'category__name': ['exact'],
        'category__subcategory': ['exact'],
        'date': ['gte','lte']
    }
  
  order_by = OrderingFilter(
    fields = (
      ('amount','amount'),
      ('date','date'),
      ('description','description'),
    )
  )