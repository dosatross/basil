import datetime
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from basil.apps.categories.models import Category, CategoryGroup
from basil.apps.categories.api.serializers import CategorySerializer, CategoryGroupSerializer
from basil.apps.categories.api.utils import filter_categories_by_category_set


class CategoryViewSet(viewsets.ModelViewSet):

	serializer_class = CategorySerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		return Category.objects.filter(user=user)

	def list(self,request):
		q = filter_categories_by_category_set(self.get_queryset(),request.query_params.get('set'))
		if not q:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		serializer = CategorySerializer(q, many=True)
		return Response(serializer.data)

class CategoryGroupViewSet(viewsets.ModelViewSet):

	serializer_class = CategoryGroupSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		return CategoryGroup.objects.filter(user=user)