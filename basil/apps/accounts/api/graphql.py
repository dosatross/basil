from graphene import ObjectType, Field, ID
from graphene_django import DjangoObjectType
from graphene_subscriptions.events import UPDATED

from basil.apps.accounts.models import BasilUser

class UserType(DjangoObjectType):
  class Meta:
    model = BasilUser

class UserProfileQuery(ObjectType):
  profile = Field(UserType)

  def resolve_profile(self, info, **kwargs):
    user = info.context.user
    return user

class UserProfileSubscription(ObjectType):
    profile = Field(UserType, id=ID(required=True))

    def resolve_profile(root, info, id):
      return root.filter(
          lambda event:
              event.operation == UPDATED and
              isinstance(event.instance, BasilUser) and
              event.instance.pk == int(id)
      ).map(lambda event: event.instance)