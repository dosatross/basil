from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Basil API Docs')),
    path('api-auth/', include('rest_framework.urls')),
]


api_urlpatterns = [
	path('auth/token-auth/', obtain_auth_token),
	path('auth/jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	re_path('accounts/', include('basil.apps.accounts.api.urls')),
	re_path('transactions/', include('basil.apps.transactions.api.urls')),
	re_path('categories/', include('basil.apps.categories.api.urls')),
]

urlpatterns += [
	re_path('api/', include(api_urlpatterns))
]



if 'debug_toolbar' in settings.INSTALLED_APPS:
	import debug_toolbar
	urlpatterns += [
		path('__debug__/', include(debug_toolbar.urls)),
		path('silk/', include('silk.urls', namespace='silk')),
	]