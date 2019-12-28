from datetime import datetime as dt
from django.db.models import Q, Func, F

from basil.apps.transactions.constants import ISO_DATE_FORMAT, PERIOD_WEEK, PERIOD_MONTH, PERIOD_QUARTER,PERIOD_YEAR, PERIOD_LENGTHS
from basil.apps.categories.models import Category, CategoryGroup


def filter_category_set(set,group_name=None,include=None,exclude=None):
  # get base category set
  if set == 'income':
    category_set = Category.get_income_categories()
  elif set == 'expenses':
    category_set = Category.get_expense_categories()
  elif set == 'group':
    if not group_name or not CategoryGroup.objects.filter(name=group_name).first():
      return None
    else:
      category_set = CategoryGroup.objects.filter(name=group_name).first().categories.all()
  elif set == 'transactions':
    category_set = Category.objects.all()
  else:
    return None
  
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

def filter_transactions(qs,date_range=None,top=None):
  if date_range:
    date_range = parse_date_range(date_range)
    qs = qs.filter(date__range=[date_range['start'], date_range['end']])
  if top:
    qs = qs.annotate(abs=Func(F('amount'), function='ABS')).order_by('-abs')[:int(top)]
  return qs