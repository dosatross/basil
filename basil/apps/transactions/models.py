from django.db import models
from django.db.models import Sum
from basil.apps.categories.models import Category


class Transaction(models.Model):
	amount = models.DecimalField(decimal_places=2, max_digits=11)
	description = models.CharField(max_length=150, null=True)
	category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
	date = models.DateField()

	class Meta:
		ordering = ['-date']

	def get_sum_over_period(trunc,categories):
		return Transaction.objects.filter(category__in=categories) \
			.annotate(period=trunc('date')) \
			.values('period') \
			.annotate(total=Sum('amount')) \
			.order_by('-period')