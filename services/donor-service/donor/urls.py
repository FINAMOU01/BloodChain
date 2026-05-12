from django.urls import path
from .views import DonorCreateView, DonorProfileView

urlpatterns = [
    path('register/', DonorCreateView.as_view(), name='donor-register'),
    path('profile/<str:email>/', DonorProfileView.as_view(), name='donor-profile'),
]
