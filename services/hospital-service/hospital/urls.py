from django.urls import path
from .views import BloodRequestCreateView, BloodRequestListView, BloodStockView

urlpatterns = [
    path('request/', BloodRequestCreateView.as_view(), name='blood-request-create'),
    path('requests/', BloodRequestListView.as_view(), name='blood-request-list'),
    path('stock/<int:hospital_id>/', BloodStockView.as_view(), name='blood-stock'),
]

