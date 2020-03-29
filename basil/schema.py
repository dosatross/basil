import logging
from django.conf import settings
from graphene import Schema, ObjectType, Field
from graphene.relay import Node
import graphql_jwt
from graphene_django import DjangoObjectType

from basil.apps.accounts.api.graphql import UserProfileQuery
from basil.apps.transactions.api.graphql import (TransactionQuery, DateRangeQuery, 
    PeriodTotalQuery, CategoryTotalQuery, PeriodCategoryTotalQuery, CategoryPeriodTotalQuery, CategorySetPeriodTotalQuery)
from basil.apps.categories.api.graphql import CategoryQuery, CategoryGroupQuery, CategoryMutation, CategoryGroupMutation
from basil.apps.transactions.api.graphql import TransactionMutation, ImportTransactionCsvMutation

from graphene_django.debug import DjangoDebug

class Query(UserProfileQuery,
            TransactionQuery,
            CategoryQuery,
            CategoryGroupQuery,
            DateRangeQuery, 
            PeriodTotalQuery, 
            CategoryTotalQuery, 
            PeriodCategoryTotalQuery, 
            CategoryPeriodTotalQuery, 
            CategorySetPeriodTotalQuery,
            ObjectType):
  node = Node.Field()
  
  if settings.DEBUG:
    debug = Field(DjangoDebug, name='_debug')
    

class Mutation(ObjectType):
  transaction_create = TransactionMutation.CreateField()
  transaction_delete = TransactionMutation.DeleteField()
  transaction_update = TransactionMutation.UpdateField()
  importTransactionCsv = ImportTransactionCsvMutation.Field()

  category_group_create = CategoryGroupMutation.CreateField()
  category_group_delete = CategoryGroupMutation.DeleteField()
  category_group_update = CategoryGroupMutation.UpdateField()

  category_create = CategoryMutation.CreateField()
  category_delete = CategoryMutation.DeleteField()
  category_update = CategoryMutation.UpdateField()

  token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()

schema = Schema(query=Query, mutation=Mutation)

"""
Graphene Django Issues
PrimaryKeyRelatedField support needed for CategoryGroupSerializer:
https://github.com/graphql-python/graphene-django/issues/389 


N+1 problem foreign keys
https://github.com/graphql-python/graphene-django/issues/57

With Resolution
No validation at graphene level
https://github.com/graphql-python/graphene/issues/777
Use cerberus as validation layer

Filtering and pagination relies on relay / no offset-limit pagination:
https://github.com/graphql-python/graphene-django/issues/206
https://github.com/graphql-python/graphene-django/issues/274
offset-limit pagination can be acheived with connections/cursors

"""