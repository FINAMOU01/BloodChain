from django.urls import path
from .views import MintRewardView, RewardListView

urlpatterns = [
    path('mint/', MintRewardView.as_view(), name='mint-reward'),
    path('list/', RewardListView.as_view(), name='reward-list'),
]
