from django.urls import path
from .views import DonorCreateView, DonorProfileView, DonorListView, DonorUpdateView, AppointmentListView, AppointmentCreateView, AppointmentUpdateView, DonorEligibilityView

urlpatterns = [
    path('register/', DonorCreateView.as_view(), name='donor-register'),
    path('list/', DonorListView.as_view(), name='donor-list'),
    path('profile/<str:email>/', DonorProfileView.as_view(), name='donor-profile'),
    path('profile/<str:email>/update/', DonorUpdateView.as_view(), name='donor-update'),
    path('appointments/<str:donor_email>/', AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointments/<int:pk>/update/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('eligibility/<str:donor_email>/', DonorEligibilityView.as_view(), name='donor-eligibility'),
]
