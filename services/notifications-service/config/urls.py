from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

def health(request):
    return JsonResponse({'status': 'ok'})

schema_view = get_schema_view(
    openapi.Info(
        title='Notifications Service API',
        default_version='v1',
        description='BloodChain Notifications Microservice',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('health/', health),
    path('', include('django_prometheus.urls')),
    path('admin/', admin.site.urls),
    path('api/notifications/', include('app.urls')),
    path('api/docs/', schema_view.with_ui('swagger'), name='swagger-ui'),
]
