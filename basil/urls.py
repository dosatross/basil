from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Basil API Docs')),
]


api_urlpatterns = [
	re_path('transactions/', include('basil.apps.transactions.api.urls')),
	re_path('categories/', include('basil.apps.categories.api.urls')),
]

urlpatterns += [
	re_path('api/', include(api_urlpatterns))
]