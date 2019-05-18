import datetime
import json
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from django.middleware.csrf import get_token
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import api_view
from basil.apps.accounts.models import BasilUser
from basil.apps.accounts.api.serializers import UserSerializer, UserProfileSerializer


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
	body = json.loads(request.body)
	email = body.get("email", "")
	password = body.get("password", "")
	user = authenticate(request, email=email, password=password)
	if user is not None:
		login(request, user)
		return JsonResponse({
			'userid': user.id,
			'sessionid': request.session.session_key,
			'csrftoken': get_token(request)
		})
	return HttpResponse(status=400)

def logout_view(request):
	try:
		logout(request)
		return HttpResponse()
	except AttributeError:
		return HttpResponse(status=400)

class UserViewSet(viewsets.ModelViewSet):

	serializer_class = UserSerializer
	queryset = BasilUser.objects.all()
	permission_classes = (permissions.IsAdminUser,)

class UserProfileView(generics.RetrieveUpdateAPIView):

	serializer_class = UserProfileSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self):
		return self.request.user