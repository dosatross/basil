import os
from django.core.management.base import BaseCommand, CommandError
from basil.apps.accounts.models import BasilUser
from basil.settings import BASE_DIR

from basil.apps.transactions.services import import_transactions_csv

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
		parser.add_argument(
			'--email',
			dest='email',
			default='demo@gmail.com'
			)

	def handle(self, *args, **options):
		user = BasilUser.objects.get(email=options['email'])
		import_transactions_csv(user,options['transactions'],options['categories_map'],options['source'],print_progress=True,replace=True)