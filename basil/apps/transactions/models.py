from django.db import models
from basil.apps.categories.models import Category

class Transaction(models.Model):
	amount = models.IntegerField()
	description = models.CharField(max_length=500, null=True)
	category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
	date = models.DateField()

	class Meta:
		ordering = ['-date']

	def is_valid():
		pass
		

	def get_monthly_expense():
		pass
		#https://stackoverflow.com/questions/8746014/django-group-by-date-day-month-year