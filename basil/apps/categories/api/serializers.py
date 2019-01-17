from rest_framework import serializers
from basil.apps.categories.models import Category, CategoryGroup

class CategoryGroupSerializer(serializers.ModelSerializer):
	categories = serializers.SerializerMethodField()

	class Meta:
		model = CategoryGroup
		fields = '__all__'

	def get_categories(self, obj):
		return [category.name + ' - ' + category.subcategory for category in obj.categories.all()]


class CategorySerializer(serializers.ModelSerializer):
	groups = serializers.SerializerMethodField()

	def validate(self, data):
		if data.get('is_credit') == None and not data.get('is_internal'):
			raise serializers.ValidationError('Only internal categories can have null is_credit')
		return data

	class Meta:
		model = Category
		fields = '__all__'

	def get_groups(self, obj):
		return [group.name for group in obj.groups.all()]

