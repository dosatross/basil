from django.contrib import admin
from basil.apps.categories.models import Category, CategoryGroup

admin.site.register(Category)
admin.site.register(CategoryGroup)