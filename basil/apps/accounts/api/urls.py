from django.urls import path
from basil.apps.accounts.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
	path('profile/', views.ProfileView.as_view())
]

router.register('users', views.UserViewSet)

urlpatterns += router.urls