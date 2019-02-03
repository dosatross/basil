import datetime
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from basil.apps.categories.models import Category, CategoryGroup
from basil.apps.categories.api.serializers import CategorySerializer, CategoryGroupSerializer


class CategoryViewSet(viewsets.ModelViewSet):

	serializer_class = CategorySerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		return Category.objects.filter(user=user)

	def list(self,request):
		q = self.get_queryset()
		if request.query_params.get('set') == 'income':
			q = q.intersection(Category.get_income_categories())
		elif request.query_params.get('set') == 'expenses':
			q = q.intersection(Category.get_expense_categories())
		elif request.query_params.get('set'):
			return Response(status=status.HTTP_400_BAD_REQUEST)

		serializer = CategorySerializer(q, many=True)
		return Response(serializer.data)



class CategoryGroupViewSet(viewsets.ModelViewSet):

	serializer_class = CategoryGroupSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		return CategoryGroup.objects.filter(user=user)