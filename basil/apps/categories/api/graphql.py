from graphene import relay, ObjectType, List, Field, ID, String, Boolean, Int
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django_extras import DjangoSerializerMutation
import graphene_django_optimizer as gql_optimizer

from basil.utils.graphql import Connection
from basil.apps.categories.models import Category, CategoryGroup
from basil.apps.categories.api.serializers import CategorySerializer, CategoryGroupSerializer
from basil.apps.categories.api.utils import filter_categories_by_category_set


class CategoryConnection(Connection):
  class Meta:
    abstract = True

class CategoryType(DjangoObjectType):
  is_credit = Field(Int,required=False)
  class Meta:
    model = Category
    interfaces = (relay.Node, )
    filter_fields = []
    connection_class = CategoryConnection
  
  @classmethod
  def get_node(cls, info, id):
    return Category.objects.get(id=id)

class CategoryQuery(ObjectType):
  category_connection = DjangoFilterConnectionField(CategoryType)

  def resolve_category_connection(self, info, category_set=None, **kwargs):
    qs = Category.objects.filter(user=info.context.user)
    return gql_optimizer.query(filter_categories_by_category_set(qs,category_set),info)

class CategoryMutation(DjangoSerializerMutation):

  @classmethod
  def get_serializer_kwargs(cls, root, info, **kwargs):
    return {'context': {'request': info.context}}

  class Meta:
    serializer_class = CategorySerializer
    exclude_fields = ('user', )
    input_field_name = 'input'



class CategoryGroupConnection(Connection):
  class Meta:
    abstract = True

class CategoryGroupType(DjangoObjectType):
  class Meta:
    model = CategoryGroup
    interfaces = (relay.Node, )
    filter_fields = []
    connection_class = CategoryGroupConnection
  
  @classmethod
  def get_node(cls, info, id):
    return CategoryGroup.objects.get(id=id)

class CategoryGroupQuery(ObjectType):
  category_group_connection = DjangoFilterConnectionField(CategoryGroupType)

  def resolve_category_group_connection(self, info, **kwargs):
    return gql_optimizer.query(CategoryGroup.objects.filter(user=info.context.user),info)

class CategoryGroupMutation(DjangoSerializerMutation):

  @classmethod
  def get_serializer_kwargs(cls, root, info, **kwargs):
    return {'context': {'request': info.context}}

  class Meta:
    serializer_class = CategoryGroupSerializer
    exclude_fields = ('user', )
    input_field_name = 'input'