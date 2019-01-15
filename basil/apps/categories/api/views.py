import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from basil.apps.categories.models import Category
from basil.apps.categories.api.serializers import CategorySerializer


class CategoriesViewSet(viewsets.ModelViewSet):

	serializer_class = CategorySerializer
	queryset = Category.objects.all()
