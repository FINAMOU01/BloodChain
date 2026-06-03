"""
URL configuration for rewards service.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Import app URLs
try:
    from app import urls as app_urls
except ImportError:
    app_urls = None

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('metrics/', include('django_prometheus.urls')),
]

if app_urls:
    urlpatterns += [
        path('api/rewards/', include(app_urls)),
    ]
