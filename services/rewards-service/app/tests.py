from django.test import TestCase
from .models import Reward, Redemption

class RewardTestCase(TestCase):
    def setUp(self):
        Reward.objects.create(donor_id='donor_001', points=100, reason='Blood donation')

    def test_reward_creation(self):
        reward = Reward.objects.get(donor_id='donor_001')
        self.assertEqual(reward.points, 100)


class RedemptionTestCase(TestCase):
    def setUp(self):
        Redemption.objects.create(donor_id='donor_001', reward='Gift Card')

    def test_redemption_creation(self):
        redemption = Redemption.objects.get(donor_id='donor_001')
        self.assertEqual(redemption.reward, 'Gift Card')
