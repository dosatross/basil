import logging
from graphene import Schema, ObjectType
from graphene.relay import Node
import graphql_jwt
from graphene_django import DjangoObjectType
from basil.apps.accounts.api.graphql import UserProfileQuery
from basil.apps.transactions.api.graphql import (TransactionQuery, DateRangeQuery, 
    PeriodTotalQuery, CategoryTotalQuery, PeriodCategoryTotalQuery, CategoryPeriodTotalQuery, CategorySetPeriodTotalQuery)
from basil.apps.categories.api.graphql import CategoryQuery, CategoryGroupQuery, CategoryMutation, CategoryGroupMutation
from basil.apps.transactions.api.graphql import TransactionMutation

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
    

class Mutation(ObjectType):
  transaction_create = TransactionMutation.CreateField()
  transaction_delete = TransactionMutation.DeleteField()
  transaction_update = TransactionMutation.UpdateField()

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
No validation at graphene level
https://github.com/graphql-python/graphene/issues/777
Filtering and pagination relies on relay / no offset-limit pagination:
https://github.com/graphql-python/graphene-django/issues/206
https://github.com/graphql-python/graphene-django/issues/274


"""