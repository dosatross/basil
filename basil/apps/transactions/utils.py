import datetime as dt
import pandas as pd
from datetime_truncate import truncate
import basil.apps.transactions.models as t_models
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
	
def date_start_end():
	# BUG: filter by user
	start = t_models.Transaction.objects.earliest('date').date
	end = t_models.Transaction.objects.latest('date').date
	return {'start':start,'end':end}

def date_starting_periods(period_len):
	start_end = date_start_end()
	start = start_end['start']
	end = start_end['end']
	start_trunc = truncate(dt.datetime.combine(start, dt.datetime.min.time()), PY_TRUNC[period_len])
	end_trunc = truncate(dt.datetime.combine(end, dt.datetime.min.time()), PY_TRUNC[period_len])
	date_index = pd.period_range(start=start_trunc, end=end_trunc, freq=period_len.upper()).to_timestamp()
	return date_index.date