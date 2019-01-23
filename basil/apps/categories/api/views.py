import datetime
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from basil.apps.categories.models import Category, CategoryGroup
from basil.apps.categories.api.serializers import CategorySerializer, CategoryGroupSerializer


class CategoryViewSet(viewsets.ModelViewSet):

	serializer_class = CategorySerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		return Category.objects.filter(user=user)

class CategoryGroupViewSet(viewsets.ModelViewSet):

	serializer_class = CategoryGroupSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		return CategoryGroup.objects.filter(user=user)