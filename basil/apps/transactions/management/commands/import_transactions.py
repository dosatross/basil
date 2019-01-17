import os
import csv
import pytz
import datetime as dt
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from basil.apps.transactions.models import Transaction
from basil.apps.categories.models import Category
from basil.apps.transactions.api.serializers import TransactionSerializer
from basil.settings import BASE_DIR,TIME_ZONE

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
			'--transactions',
			dest='transactions',
			default=os.path.join(BASE_DIR,'apps','transactions','fixtures','transactions.csv')
			)
		parser.add_argument(
			'--categories_map',
			dest='categories_map',
			default=os.path.join(BASE_DIR,'apps','categories','fixtures','categories_map.csv')
			)
		parser.add_argument(
			'--source',
			dest='source',
			default='pb'
			)

	def handle(self, *args, **options):
		with open(options['transactions']) as tf, open(options['categories_map']) as cf:
			transactions = csv.DictReader(tf)
			categories_map = csv.DictReader(cf)
			added_transactions = []
			source = options['source']
			timezone = pytz.timezone(TIME_ZONE)

			for transaction in transactions:
				categorystr = transaction['category'].split(" - ")[0]
				subcategory = transaction['category'].split(" - ")[1]
				category = Category.objects.filter(Q(name=categorystr) & Q(subcategory=subcategory)).first()

				if not category: # check if a basil category
					for category_map in categories_map:
						# check if a source category
						if not categorystr + subcategory == category_map[source + '_category'] + category_map[source + '_subcategory']:
							print("New category " + categorystr + " - " + subcategory + " detected. New categories must be added before importing transactions.")
							for t in added_transactions:
								t.delete()
							return
						else:
							# get mapped basil category
							categorystr = category_map['basil_category'].split(" - ")[0]
							subcategory = category_map['basil_category'].split(" - ")[1]
							category = Category.objects.filter(Q(name=categorystr) & Q(subcategory=subcategory)).first()
							if not category:
								print("New category " + categorystr + " - " + subcategory + " detected. New categories must be added before importing transactions.")
								for t in added_transactions:
									t.delete()
								return
							break


				date = timezone.localize(dt.datetime.strptime(transaction['date'],"%d/%m/%Y"))
				amount = float(transaction['amount'])
				description = transaction['description']

				serializer = TransactionSerializer(data={
					'date': date.date(), 'amount': amount,
					'category': category.id,'description': description
					})
				if not serializer.is_valid():
					print(serializer.errors)
					for t in added_transactions:
						t.delete()
					return

				
				new_transaction = Transaction.objects.create(date=date,category=category,amount=amount, description=description)
				added_transactions.append(new_transaction)
				print(date)