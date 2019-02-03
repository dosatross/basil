from rest_framework import serializers
from basil.apps.transactions.models import Transaction
from basil.apps.categories.models import Category
from basil.apps.categories.api.serializers import SimpleCategorySerializer

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
				'A transaction with negative amount cannot be added to a non internal credit category. Category: ' + str(data.get('category')) + ' Date: ' + str(data.get('date'))  + ' Amount: ' + str(data.get('amount')) + ' Description: ' + str(data.get('description')))
		if not category.is_credit and not category.is_internal and data.get('amount') > 0:
			raise serializers.ValidationError(
				'A transaction with positive amount cannot be added to a non internal debit category. Category: ' + str(data.get('category')) + ' Date: ' + str(data.get('date'))  + ' Amount: ' + str(data.get('amount')) + ' Description: ' + str(data.get('description')))
		return data

class PeriodTotalTransactionSerializer(serializers.Serializer):
	total = serializers.DecimalField(decimal_places=2, max_digits=11)
	period = serializers.DateField()

class CategoryTotalTransactionSerializer(serializers.Serializer):
	total = serializers.DecimalField(decimal_places=2, max_digits=11)

	category_display = serializers.SerializerMethodField()
	category = serializers.SerializerMethodField()

	def get_category(self, obj):
		return obj['category__id']

	def get_category_display(self, obj):
		if obj['category__name'] and obj['category__subcategory']:
			return obj['category__name'] + ' - ' + obj['category__subcategory']

class PeriodCategoryTotalTransactionSerializer(serializers.Serializer):
	period = serializers.DateField()
	categories = CategoryTotalTransactionSerializer(many=True)

class CategoryPeriodTotalTransactionSerializer(serializers.Serializer):
	category = SimpleCategorySerializer()
	periods = PeriodTotalTransactionSerializer(many=True)