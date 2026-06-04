from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonationStatViewSet, HospitalDemandViewSet

router = DefaultRouter()
router.register(r'donation-stats', DonationStatViewSet)
router.register(r'hospital-demands', HospitalDemandViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
