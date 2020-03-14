from basil.apps.categories.models import Category

def filter_categories_by_category_set(qs,category_set):
    if category_set == 'income':
      qs = qs.intersection(Category.get_income_categories())
    elif category_set == 'expenses':
      qs = qs.intersection(Category.get_expense_categories())
    elif category_set:
      return None 
    return qs