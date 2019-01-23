from django.db import models
from django.db.models import Q, Sum
from django.contrib.auth.models import User
from basil.apps.categories.models import Category


class Transaction(models.Model):
	amount = models.DecimalField(decimal_places=2, max_digits=11)
	description = models.CharField(max_length=150, null=True)
	category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
	date = models.DateField()

	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-date']

	def get_sum_over_period(user,trunc,categories):
		return Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
			.annotate(period=trunc('date')) \
			.values('period') \
			.annotate(total=Sum('amount')) \
			.order_by('-period')