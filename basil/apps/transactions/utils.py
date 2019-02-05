import datetime as dt
from datetime_truncate import truncate
from django.db.models.functions import TruncWeek, TruncMonth, TruncQuarter, TruncYear
import basil.apps.transactions.models


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
	start = models.Transaction.objects.earliest('date').date
	end = models.Transaction.objects.latest('date').date
	return {'start':start,'end':end}

def date_starting_periods(period_len):
	start_end = date_start_end()
	start = start_end['start']
	end = start_end['end']
	start_trunc = truncate(dt.datetime.combine(start, dt.datetime.min.time()), get_py_trunc(period_len))
	end_trunc = truncate(dt.datetime.combine(end, dt.datetime.min.time()), get_py_trunc(period_len))
	date_index = pd.period_range(start=start_trunc, end=end_trunc, freq=period_len.upper()).to_timestamp()
	return date_index.date

def get_py_trunc(period_len):
	if period_len == PERIOD_WEEK: trunc = 'week'
	if period_len == 'm': trunc = 'month'
	if period_len == 'q': trunc = 'quarter'
	if period_len == 'y': trunc = 'year'
	return trunc

def get_trunc(period_len):
	if period_len == PERIOD_WEEK: trunc = TruncWeek
	if period_len == 'm': trunc = TruncMonth
	if period_len == 'q': trunc = TruncQuarter
	if period_len == 'y': trunc = TruncYear
	return trunc