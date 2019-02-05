from django.db.models.functions import TruncWeek, TruncMonth, TruncQuarter, TruncYear

ISO_DATE_FORMAT = '%Y-%m-%d'

PERIOD_WEEK = 'w'
PERIOD_MONTH = 'm'
PERIOD_QUARTER = 'q'
PERIOD_YEAR = 'y'

PERIOD_LENGTHS = [PERIOD_WEEK,PERIOD_MONTH,PERIOD_QUARTER,PERIOD_YEAR]

DJ_TRUNC = {
	PERIOD_WEEK: TruncWeek,
	PERIOD_MONTH: TruncMonth,
	PERIOD_QUARTER: TruncQuarter,
	PERIOD_YEAR: TruncYear
}

PY_TRUNC = {
	PERIOD_WEEK: 'week',
	PERIOD_MONTH: 'month',
	PERIOD_QUARTER: 'quarter',
	PERIOD_YEAR: 'year'
}