import datetime
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from basil.apps.categories.models import Category, CategoryGroup
from basil.apps.categories.api.serializers import CategorySerializer, CategoryGroupSerializer


class CategoryViewSet(viewsets.ModelViewSet):

	serializer_class = CategorySerializer
	queryset = Category.objects.all()
	permission_classes = (permissions.IsAuthenticated,)

class CategoryGroupViewSet(viewsets.ModelViewSet):

	serializer_class = CategoryGroupSerializer
	queryset = CategoryGroup.objects.all()
	permission_classes = (permissions.IsAuthenticated,)
