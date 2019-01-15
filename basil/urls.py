from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
]


api_urlpatterns = [
	re_path('transactions/', include('basil.apps.transactions.api.urls')),
	re_path('categories/', include('basil.apps.categories.api.urls')),
]

urlpatterns += [
	re_path('api/', include(api_urlpatterns))
]