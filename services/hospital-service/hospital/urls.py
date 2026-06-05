from django.urls import path
from .views import (
    HospitalProfileView, HospitalUpdateView, HospitalCreateView,
    BloodRequestCreateView, BloodRequestListView, BloodRequestDetailView,
    BloodRequestUpdateView, BloodStockView, BloodStockUpdateView
)

urlpatterns = [
    path('register/', HospitalCreateView.as_view(), name='hospital-create'),
    path('profile/<str:email>/', HospitalProfileView.as_view(), name='hospital-profile'),
    path('profile/<str:email>/update/', HospitalUpdateView.as_view(), name='hospital-update'),
    path('request/', BloodRequestCreateView.as_view(), name='blood-request-create'),
    path('requests/', BloodRequestListView.as_view(), name='blood-request-list'),
    path('requests/<int:pk>/', BloodRequestDetailView.as_view(), name='blood-request-detail'),
    path('requests/<int:pk>/update/', BloodRequestUpdateView.as_view(), name='blood-request-update'),
    path('stock/<int:hospital_id>/', BloodStockView.as_view(), name='blood-stock'),
    path('stock/<int:hospital_id>/update/', BloodStockUpdateView.as_view(), name='blood-stock-update'),
]
