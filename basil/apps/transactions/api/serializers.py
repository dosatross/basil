from rest_framework import serializers
from basil.apps.transactions.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
	category = serializers.SerializerMethodField()

	class Meta:
		model = Transaction
		fields = '__all__'

	def get_category(self, obj):
		return obj.category.name + ' - ' + obj.category.subcategory

class PeriodTransactionSerializer(serializers.Serializer):
	total = serializers.DecimalField(decimal_places=2, max_digits=11)
	period = serializers.DateField()
