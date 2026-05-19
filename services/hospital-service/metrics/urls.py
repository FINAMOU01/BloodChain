from django.urls import path, include

urlpatterns = [
    path('metrics/', include('django_prometheus.urls')),
]
