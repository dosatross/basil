from graphene import ObjectType, List, Field, ID, String
from graphene_django.types import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation

from basil.apps.categories.models import Category, CategoryGroup
from basil.apps.categories.api.serializers import CategorySerializer, CategoryGroupSerializer
from basil.apps.categories.api.utils import filter_categories_by_category_set

class CategoryType(DjangoObjectType):
  class Meta:
    model = Category

class CategoryQuery(ObjectType):
  category = Field(CategoryType,id=ID(required=True))
  all_categories = List(CategoryType, category_set=String())

  def resolve_category(self, info, id):
    return Category.objects.get(id=id)

  def resolve_all_categories(self, info, category_set):
    qs = Category.objects.filter(user=info.context.user)
    return filter_categories_by_category_set(qs,category_set)

class CategoryMutation(SerializerMutation):
  class Meta:
    serializer_class = CategorySerializer


class CategoryGroupType(DjangoObjectType):
  class Meta:
    model = CategoryGroup

class CategoryGroupQuery(ObjectType):
  category_group = Field(CategoryGroupType,id=ID(required=True))
  all_category_groups = List(CategoryGroupType)

  def resolve_category_group(self, info, id):
    return CategoryGroup.objects.get(id=id)

  def resolve_all_category_groups(self, info, **kwargs):
    return CategoryGroup.objects.filter(user=info.context.user)

class CategoryGroupMutation(SerializerMutation):
  class Meta:
    serializer_class = CategoryGroupSerializer