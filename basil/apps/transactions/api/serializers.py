from rest_framework import serializers
from basil.apps.transactions.models import Transaction
from basil.apps.categories.models import Category

class TransactionSerializer(serializers.ModelSerializer):
	category_display = serializers.SerializerMethodField()
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = Transaction
		fields = '__all__'

	def get_category_display(self, obj):
		if obj.category:
			return str(obj.category)

	def validate(self, data):
		category = data.get('category')
		if category.is_credit and not category.is_internal and data.get('amount') < 0:
			raise serializers.ValidationError(
				'A transaction with negative amount cannot be added to a non internal credit category.')
		if not category.is_credit and not category.is_internal and data.get('amount') > 0:
			raise serializers.ValidationError(
				'A transaction with positive amount cannot be added to a non internal debit category.')
		return data

class PeriodTransactionSerializer(serializers.Serializer):
	total = serializers.DecimalField(decimal_places=2, max_digits=11)
	period = serializers.DateField()
