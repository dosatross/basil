import csv
import os
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from basil.apps.categories.models import Category, CategoryGroup
from basil.apps.categories.api.serializers import CategorySerializer
from basil.settings import BASE_DIR

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
			'--file',
			dest='file',
			default=os.path.join(BASE_DIR,'apps','categories','fixtures','categories.csv')
			)
		parser.add_argument(
			'--username',
			dest='username',
			default='demo'
			)

	def handle(self, *args, **options):
		with open(options['file']) as csvfile:
			reader = csv.DictReader(csvfile)
			group_list = [element for element in reader.fieldnames if element not in ["category","subcategory","is_credit","is_adjustment","is_internal"]]
			added_categories = []
			user = User.objects.get(username=options['username'])

			for row in reader:
				categorystr = row['category']
				subcategory = row['subcategory']

				# continue if category exists
				category = Category.objects.filter(Q(name=categorystr) & Q(subcategory=subcategory) & Q(user=user)).first()
				if category:
					continue

				is_credit_str = row['is_credit']
				is_adjustment_str = row['is_adjustment']
				is_internal_str = row['is_internal']

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


				# validate data
				# mock request to simulate current user
				factory = APIRequestFactory()
				factory = request = factory.get('')
				request.user = user
				context = {"request": request}
				serializer = CategorySerializer(data={
					'name': categorystr, 'subcategory': subcategory,'is_credit': is_credit, 
					'is_adjustment': is_adjustment,'is_internal': is_internal
					}, context=context)
				if not serializer.is_valid():
					print(serializer.errors)
					for c in added_categories:
						c.delete()
					return


				new_category = Category.objects.create(name=categorystr, subcategory=subcategory, 
					is_credit=is_credit,is_adjustment=is_adjustment, is_internal=is_internal, user=user)
				

				# add groups
				for group_name in group_list:
					if row[group_name] == "TRUE":
						new_category.groups.add(CategoryGroup.objects.get(name=group_name, user=user))

				added_categories.append(new_category)
				print(new_category)
