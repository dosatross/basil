from django.urls import path
from basil.apps.accounts.api import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()

urlpatterns = [
	path('profile/', views.UserProfileView.as_view()),
    path('token-auth/', obtain_auth_token)
]


router.register('users', views.UserViewSet)

urlpatterns += router.urls