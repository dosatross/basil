from django.db import models
from basil.apps.accounts.models import BasilUser
from basil.apps.institutions.models import Institution

class TransactionAccount(models.Model):
  name = models.CharField(max_length=50, null=False, blank=False)
  institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
  user = models.ForeignKey(BasilUser, on_delete=models.CASCADE)

  class Meta:
    ordering = ['name']

  def __str__(self):
    return f'{self.name}'
