from django.urls import path
from basil.apps.accounts.api import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()

urlpatterns = [
	path('profile/', views.UserProfileView.as_view()),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]


router.register('users', views.UserViewSet)

urlpatterns += router.urls