from django.urls import path
from .views import BloodBagCreateView, BloodBagDetailView, BloodBagDonorListView

urlpatterns = [
    path('bag/collect/', BloodBagCreateView.as_view(), name='bag-collect'),
    path('bag/<str:bag_id>/', BloodBagDetailView.as_view(), name='bag-detail'),
    path('bags/donor/<str:donor_email>/', BloodBagDonorListView.as_view(), name='bags-by-donor'),
]
