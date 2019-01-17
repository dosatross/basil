from django.urls import path
from basil.apps.categories.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('categories', views.CategoryViewSet)
router.register('groups', views.CategoryGroupViewSet)

urlpatterns = router.urls