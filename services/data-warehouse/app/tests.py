from django.test import TestCase
from datetime import date
from .models import DonationStat, HospitalDemand

class DonationStatTestCase(TestCase):
    def setUp(self):
        DonationStat.objects.create(
            date=date.today(),
            total_donations=100,
            blood_type='O+',
            region='North'
        )

    def test_donation_stat_creation(self):
        stat = DonationStat.objects.get(blood_type='O+')
        self.assertEqual(stat.total_donations, 100)


class HospitalDemandTestCase(TestCase):
    def setUp(self):
        HospitalDemand.objects.create(
            date=date.today(),
            hospital_id='hospital_001',
            blood_type='A+',
            units_needed=50
        )

    def test_hospital_demand_creation(self):
        demand = HospitalDemand.objects.get(hospital_id='hospital_001')
        self.assertEqual(demand.units_needed, 50)
