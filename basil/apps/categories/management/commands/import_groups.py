import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.contrib.auth.models import User
from basil.apps.categories.models import Category, CategoryGroup
from basil.settings import BASE_DIR

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
			'--file',
			dest='file',
			default=os.path.join(BASE_DIR,'apps','categories','fixtures','groups.csv')
			)
		parser.add_argument(
			'--username',
			dest='username',
			default='demo'
			)

	def handle(self, *args, **options):
		with open(options['file']) as csvfile:
			reader = csv.DictReader(csvfile)
			user = User.objects.get(username=options['username'])
			for row in reader:
				name = row['group']
				description = row['description']

				# skip if category exists
				category = CategoryGroup.objects.filter(name=name, user=user).first()
				if not category:
					category = CategoryGroup.objects.create(name=name, description=description, user=user)
					print(category)
