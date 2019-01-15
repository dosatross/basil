import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from basil.apps.categories.models import Category
from basil.settings import BASE_DIR

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
			'--file',
			dest='file',
			default=os.path.join(BASE_DIR,'apps','categories','categories.csv')
			)

	def handle(self, *args, **options):
		with open(options['file']) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				categorystr = row['category']
				subcategory = row['subcategory']

				# continue if category exists
				category = Category.objects.filter(Q(name=categorystr) & Q(subcategory=subcategory)).first()
				if category:
					continue

				is_credit_str = row['is_credit']
				is_adjustment_str = row['is_adjustment']
				is_internal_str = row['is_internal']
				is_earned_str = row['is_earned']

				if is_credit_str == "TRUE":
					is_credit = True
				elif is_credit_str == "FALSE":
					is_credit = False
				else:
					is_credit = None

				if is_adjustment_str == "TRUE":
					is_adjustment = True
				else:
					is_adjustment = False

				if is_internal_str == "TRUE":
					is_internal = True
				else:
					is_internal = False

				if is_earned_str == "TRUE":
					is_earned = True
				elif is_earned_str == "FALSE":
					is_earned = False
				else:
					is_earned = None

				category = Category.objects.create(name=categorystr, subcategory=subcategory, 
					is_credit=is_credit,is_adjustment=is_adjustment,
					is_internal=is_internal,is_earned=is_earned)
