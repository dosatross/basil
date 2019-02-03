from django.db import models
from django.db.models import Q, Sum, Func, F, Count
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



	def total_over_period(user,trunc,categories):
		return Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
			.annotate(period=trunc('date')) \
			.values('period') \
			.annotate(total=Sum('amount')) \
			.order_by('-period')

	def total_over_category(user,categories):
		return Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
			.values('category__id','category__name','category__subcategory') \
			.annotate(total=Sum('amount')) \
			.annotate(abs_total=Func(F('total'), function='ABS')) \
			.order_by('-abs_total')
			
	def total_over_period_and_categories(user,trunc,categories):
		q = Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
			.annotate(period=trunc('date')) \
			.values('period','category__id','category__name','category__subcategory') \
			.annotate(total=Sum('amount')) \
			.annotate(abs_total=Func(F('total'), function='ABS')) \
			.order_by('-period','-abs_total','-category__name','-category__subcategory')

		dates = q.values("period").annotate(Count("period")).order_by() # get distinct dates

		# get category totals nested in periods
		return [{'period': date['period'], \
				'categories':[o for o in q if o in q.filter(period=date['period'])]} for date in dates]