from basil.apps.accounts.models import BasilUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

@receiver(post_save, sender=BasilUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
  if created:
    Token.objects.create(user=instance)

post_save.connect(post_save_subscription, sender=BasilUser, dispatch_uid="basil_post_save")