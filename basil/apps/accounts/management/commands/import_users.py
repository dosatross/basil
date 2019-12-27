from django.core.management.base import BaseCommand, CommandError
from basil.apps.accounts.models import BasilUser

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument(
			'--create_su',
			dest='su',
			default=True
			)
		parser.add_argument(
			'--create_admin',
			dest='admin',
			default=True
			)

	def handle(self, *args, **options):
		user = BasilUser.objects.create(
			email='demo@gmail.com',
			is_superuser = False,
			is_staff = False
		)
		user.set_password('demo')
		user.save()
		print("User 'demo' created.")


		if options['su']:
			user = BasilUser.objects.create(
				email='su@gmail.com',
				is_superuser = True,
				is_staff = True
			)
			user.set_password('su')
			user.save()
			print("Superuser 'su' created.")


		if options['admin']:
			user = BasilUser.objects.create(
				email='admin@gmail.com',
				is_superuser = False,
				is_staff = True
			)
			user.set_password('admin')
			user.save()
			print("Admin user 'admin' created.")

