from django.db import models
from basil.apps.accounts.models import BasilUser

class Institution(models.Model):
	title = models.CharField(max_length=50, null=False, blank=False)
	user = models.ForeignKey(BasilUser, on_delete=models.CASCADE)

	class Meta:
		ordering = ['title']

	def __str__(self):
		return f'{self.title}'
