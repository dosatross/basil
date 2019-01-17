from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
	date_joined = serializers.DateTimeField(read_only=True,format="%Y-%m-%d")
	last_login = serializers.DateTimeField(read_only=True,format="%Y-%m-%d")

	class Meta:
		model = User
		fields = ['last_login','is_superuser','username','first_name','last_name','email','is_staff','is_active','date_joined']
		read_only_fields = ['last_login','is_superuser','is_staff','is_active','date_joined']