from django.apps import AppConfig


class AccountsConfig(AppConfig):
	name = 'basil.apps.accounts'

	def ready(self):
		import basil.apps.accounts.signals