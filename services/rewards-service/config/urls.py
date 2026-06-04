from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Rewards Service API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include('django_prometheus.urls')),
    path('admin/', admin.site.urls),
    path('api/rewards/', include('app.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('health/', lambda request: __import__('django.http', fromlist=['JsonResponse']).JsonResponse({'status': 'healthy'})),
]
