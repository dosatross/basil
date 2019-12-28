from basil.apps.categories.models import Category

def filter_categories_by_category_set(base_query,category_set):
    if category_set == 'income':
      q = base_query.intersection(Category.get_income_categories())
    elif category_set == 'expenses':
      q = base_query.intersection(Category.get_expense_categories())
    elif category_set:
      return None 
    return q