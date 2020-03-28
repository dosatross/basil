from graphene import ObjectType, Field
from graphene_django import DjangoObjectType

from basil.apps.accounts.models import BasilUser

class UserType(DjangoObjectType):
  class Meta:
    model = BasilUser

class UserProfileQuery(ObjectType):
  profile = Field(UserType)

  def resolve_profile(self, info, **kwargs):
    user = info.context.user
    return user