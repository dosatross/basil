from rest_framework import serializers
from basil.apps.categories.models import Category, CategoryGroup

class CategoryGroupSerializer(serializers.ModelSerializer):
	categories = serializers.PrimaryKeyRelatedField(many=True,queryset=Category.objects.all())
	categories_display = serializers.SerializerMethodField()
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = CategoryGroup
		fields = '__all__'
		read_only_fields = ['categories_display']
		

	def validate_categories(self, value):
		valid_categories = Category.objects.filter(user=self.context['request'].user)
		for category in value:
			if category not in valid_categories:
				raise serializers.ValidationError("Invalid category")
		return value

	def get_categories_display(self, obj):
		return [str(category) for category in obj.categories.all()]


class CategorySerializer(serializers.ModelSerializer):
	groups_display = serializers.SerializerMethodField()
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())

	class Meta:
		model = Category
		fields = '__all__'

	def get_groups_display(self, obj):
		return [group.name for group in obj.groups.all()]

	def validate(self, data):
		if data.get('is_credit') == None and not data.get('is_internal'):
			raise serializers.ValidationError('Only internal categories can have null is_credit')
		return data

class SimpleCategorySerializer(serializers.ModelSerializer):
	category_display = serializers.SerializerMethodField()

	class Meta:
		model = Category
		fields = ['id','category_display']

	def get_category_display(self, obj):
		return str(obj)

