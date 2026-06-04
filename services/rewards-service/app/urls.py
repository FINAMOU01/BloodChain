from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RewardViewSet, RedemptionViewSet

router = DefaultRouter()
router.register(r'rewards', RewardViewSet)
router.register(r'redemptions', RedemptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
