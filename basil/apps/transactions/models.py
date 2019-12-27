from django.db import models
from django.db.models import Q, Sum, Func, F, Count
from basil.apps.accounts.models import BasilUser
from basil.apps.categories.models import Category
from basil.apps.transactions.utils import *
from basil.apps.transactions.constants import DJ_TRUNC


class Transaction(models.Model):
	amount = models.DecimalField(decimal_places=2, max_digits=11)
	description = models.CharField(max_length=150, null=True)
	category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
	date = models.DateField()

	user = models.ForeignKey(BasilUser, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-date']

	def period_total(user,period_len,categories):
		q = list(Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
					.annotate(period_starting=DJ_TRUNC[period_len]('date')) \
					.values('period_starting') \
					.annotate(total=Sum('amount')) \
					.order_by('-period_starting'))

		dates = date_starting_periods(user,period_len)

		return [{'period_starting': date,'total': total_or_zero_p(q,date) } for date in dates]



	def category_total(user,categories,date_range,top=None):
		q = list(Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
					.filter(date__range=[date_range['start'].isoformat(), date_range['end'].isoformat()]) \
					.values('category__id') \
					.annotate(total=Sum('amount')) \
					.annotate(abs_total=Func(F('total'), function='ABS')) \
					.order_by('-abs_total'))

		result = [{'category': category,'total': total_or_zero_c(q,category) } for category in categories]
		result = sorted(result, key=lambda x: abs(x['total']),reverse=True) 
		if top:
			return result[:top]
		return result
			

	def period_category_total(user,period_len,categories):
		""" with category totals nested in periods """
		q = list(Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
					.annotate(period_starting=DJ_TRUNC[period_len]('date')) \
					.values('period_starting','category__id') \
					.annotate(total=Sum('amount')) \
					.annotate(abs_total=Func(F('total'), function='ABS')) \
					.order_by('-period_starting','-abs_total','-category__id'))

		dates = date_starting_periods(user,period_len)

		return [{'period_starting': date, 'categories': 
			[{'category': category,'total': total_or_zero(q,category,date)} 
				for category in categories]} for date in dates]

	def category_period_total(user,period_len,categories):
		""" 
		with period totals nested in categories
		"""
		q = list(Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
					.annotate(period_starting=DJ_TRUNC[period_len]('date')) \
					.values('period_starting','category__id') \
					.annotate(total=Sum('amount')) \
					.annotate(abs_total=Func(F('total'), function='ABS')) \
					.order_by('-period_starting','-abs_total','-category__id'))
			

		dates = date_starting_periods(user,period_len)

		return [{'category': category, 'periods_starting': 
			[{'period_starting': date,'total': total_or_zero(q,category,date)} 
				for date in dates]} for category in categories]


