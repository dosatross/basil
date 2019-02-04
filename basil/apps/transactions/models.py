import datedelta
import datetime as dt
import pandas as pd
from datetime_truncate import truncate
from django.db import models
from django.db.models import Q, Sum, Func, F, Count
from django.db.models.functions import TruncWeek, TruncMonth, TruncQuarter, TruncYear
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


	def period_total(user,period_len,categories):
		q = Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
			.annotate(period_starting=get_trunc(period_len)('date')) \
			.values('period_starting') \
			.annotate(total=Sum('amount')) \
			.order_by('-period_starting')

		dates = date_starting_periods(period_len)

		return [{'period_starting': date,'total': total_or_zero_p(q,date) } for date in dates]



	def category_total(user,categories,top):
		q = Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
			.values('category__id') \
			.annotate(total=Sum('amount')) \
			.annotate(abs_total=Func(F('total'), function='ABS')) \
			.order_by('-abs_total')

		result = [{'category': category,'total': total_or_zero_c(q,category) } for category in categories]
		if top:
			return result[:top]
		return result
			

	def period_category_total(user,period_len,categories):
		""" with category totals nested in periods """
		q = Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
			.annotate(period_starting=get_trunc(period_len)('date')) \
			.values('period_starting','category__id') \
			.annotate(total=Sum('amount')) \
			.annotate(abs_total=Func(F('total'), function='ABS')) \
			.order_by('-period_starting','-abs_total','-category__id')

		dates = date_starting_periods(period_len)

		return [{'period_starting': date, 'categories': 
			[{'category': category,'total': total_or_zero(q,category,date)} 
				for category in categories]} for date in dates]

	def category_period_total(user,period_len,categories):
		""" 
		with period totals nested in categories
		"""
		q = Transaction.objects.filter(Q(category__in=categories) & Q(user=user)) \
			.annotate(period_starting=get_trunc(period_len)('date')) \
			.values('period_starting','category__id') \
			.annotate(total=Sum('amount')) \
			.annotate(abs_total=Func(F('total'), function='ABS')) \
			.order_by('-period_starting','-abs_total','-category__id')

		dates = date_starting_periods(period_len)

		return [{'category': category, 'periods_starting': 
			[{'period_starting': date,'total': total_or_zero(q,category,date)} 
				for date in dates]} for category in categories]


def total_or_zero(q,category,period_starting):
	o = q.filter(category__id=category.id,period_starting=period_starting).first()
	if not o:
		return 0
	return o['total']

def total_or_zero_p(q,period_starting):
	o = q.filter(period_starting=period_starting).first()
	if not o:
		return 0
	return o['total']

def total_or_zero_c(q,category):
	o = q.filter(category__id=category.id).first()
	if not o:
		return 0
	return o['total']

def date_start_end():
	start = Transaction.objects.earliest('date').date
	end = Transaction.objects.latest('date').date
	return start, end

def date_starting_periods(period_len):
	start, end = date_start_end()
	start_trunc = truncate(dt.datetime.combine(start, dt.datetime.min.time()), get_py_trunc(period_len))
	end_trunc = truncate(dt.datetime.combine(end, dt.datetime.min.time()), get_py_trunc(period_len))
	date_index = pd.period_range(start=start_trunc, end=end_trunc, freq=period_len.upper()).to_timestamp()
	return date_index.date

def get_py_trunc(period_len):
	if period_len == 'w': trunc = 'week'
	if period_len == 'm': trunc = 'month'
	if period_len == 'q': trunc = 'quarter'
	if period_len == 'y': trunc = 'year'
	return trunc

def get_trunc(period_len):
	if period_len == 'w': trunc = TruncWeek
	if period_len == 'm': trunc = TruncMonth
	if period_len == 'q': trunc = TruncQuarter
	if period_len == 'y': trunc = TruncYear
	return trunc