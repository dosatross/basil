import datetime
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from basil.apps.accounts.api.serializers import UserSerializer, UserProfileSerializer


class UserViewSet(viewsets.ModelViewSet):

	serializer_class = UserSerializer
	queryset = User.objects.all()
	permission_classes = (permissions.IsAdminUser,)

class ProfileView(generics.RetrieveUpdateAPIView):

	serializer_class = UserProfileSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self):
		return self.request.user