"""
URL configuration for bloodchain user-management service.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.conf import settings
from django.views.static import serve
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

def health(request):
    return JsonResponse({'status': 'ok'})

schema_view = get_schema_view(
    openapi.Info(
        title="User Management Service API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('health/', health),
    path('', include('django_prometheus.urls')),
    path('admin/', admin.site.urls),
    path('api/users/', include('app.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
