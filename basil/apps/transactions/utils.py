import datetime as dt
import pandas as pd
from datetime_truncate import truncate
from basil.apps.transactions.constants import PY_TRUNC, PERIOD_WEEK, PERIOD_MONTH, PERIOD_QUARTER, PERIOD_YEAR


def total_or_zero(q,category,period_starting):
	for o in q:
		if o['category__id'] == category.id and o['period_starting'] == period_starting:
			return o['total']
	return 0

def total_or_zero_p(q,period_starting):
	for o in q:
		if o['period_starting'] == period_starting:
			return o['total']
	return 0

def total_or_zero_c(q,category):
	for o in q:
		if o['category__id'] == category.id:
			return o['total']
	return 0
	
def date_start_end(user):
	from basil.apps.transactions.models import Transaction
	start = Transaction.objects.filter(user=user).earliest('date').date
	end = Transaction.objects.filter(user=user).latest('date').date
	return {'start':start,'end':end}

def date_starting_periods(user,period_len):
	start_end = date_start_end(user)
	start = start_end['start']
	end = start_end['end']
	start_trunc = truncate(dt.datetime.combine(start, dt.datetime.min.time()), PY_TRUNC[period_len])
	end_trunc = truncate(dt.datetime.combine(end, dt.datetime.min.time()), PY_TRUNC[period_len])
	date_index = pd.period_range(start=start_trunc, end=end_trunc, freq=period_len.upper()).to_timestamp()
	return date_index.date