from django.urls import path
from .views import BloodBagCreateView, BloodBagDetailView

urlpatterns = [
    path('bag/collect/', BloodBagCreateView.as_view(), name='bag-collect'),
    path('bag/<str:bag_id>/', BloodBagDetailView.as_view(), name='bag-detail'),
]