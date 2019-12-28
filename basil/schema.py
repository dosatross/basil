import logging
from graphene import Schema, ObjectType
import graphql_jwt
from graphene_django import DjangoObjectType
from basil.apps.accounts.api.graphql import UserProfileQuery
from basil.apps.transactions.api.graphql import (TransactionQuery, DateRangeQuery, 
    PeriodTotalQuery, CategoryTotalQuery, PeriodCategoryTotalQuery, CategoryPeriodTotalQuery)
from basil.apps.categories.api.graphql import CategoryQuery, CategoryGroupQuery


class Query(UserProfileQuery,
            TransactionQuery,
            CategoryQuery,
            CategoryGroupQuery,
            DateRangeQuery, 
            PeriodTotalQuery, 
            CategoryTotalQuery, 
            PeriodCategoryTotalQuery, 
            CategoryPeriodTotalQuery, 
            ObjectType):
  pass
    

class Mutation(ObjectType):
  token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()

schema = Schema(query=Query, mutation=Mutation)