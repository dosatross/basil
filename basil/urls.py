from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Basil API Docs')),
    path('api-auth/', include('rest_framework.urls')), 
]


api_urlpatterns = [
	re_path('users/', include('basil.apps.accounts.api.urls')),
	re_path('transactions/', include('basil.apps.transactions.api.urls')),
	re_path('categories/', include('basil.apps.categories.api.urls')),
]

urlpatterns += [
	re_path('api/', include(api_urlpatterns))
]



if settings.DEBUG:
	import debug_toolbar
	urlpatterns += [
		path('__debug__/', include(debug_toolbar.urls)),
		path('silk/', include('silk.urls', namespace='silk')),
	]