from django.urls import path
from basil.apps.categories.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('', views.CategoriesViewSet, basename='categories')

urlpatterns = router.urls