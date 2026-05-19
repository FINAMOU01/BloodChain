from django.urls import path
from .views import EmergencyAlertView, NotificationListView

urlpatterns = [
    path('alert/', EmergencyAlertView.as_view(), name='emergency-alert'),
    path('list/', NotificationListView.as_view(), name='notification-list'),
]
