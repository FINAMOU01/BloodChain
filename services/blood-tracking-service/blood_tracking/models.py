import uuid
from django.db import models

# Create your models here.

class BloodBag(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    STATUS_CHOICES = [
        ('collected', 'collected'),
        ('tested', 'tested'),
        ('stored', 'stored'),
        ('transfused', 'transfused'),
        ('expired', 'expired'),
    ]

    bag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='collected')
    collected_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    blockchain_tx_hash = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.bag_id} ({self.status})"
