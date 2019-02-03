from django.urls import path
from basil.apps.categories.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('categories', views.CategoryViewSet, base_name="category")
router.register('groups', views.CategoryGroupViewSet, base_name="group")


urlpatterns = router.urls