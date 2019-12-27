import logging
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import models

class UserType(DjangoObjectType):
    class Meta:
         model = models.User

class Query(graphene.ObjectType):
    user = graphene.Field(UserType)

    def resolve_user(self, info, **kwargs):
      user = info.context.user
      return user

schema = graphene.Schema(query=Query)