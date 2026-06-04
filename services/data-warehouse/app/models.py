from django.db import models

class DonationStat(models.Model):
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

    date = models.DateField()
    total_donations = models.IntegerField(default=0)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES)
    region = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('date', 'blood_type', 'region')

    def __str__(self):
        return f"{self.date} - {self.blood_type} ({self.region}): {self.total_donations} donations"


class HospitalDemand(models.Model):
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

    date = models.DateField()
    hospital_id = models.CharField(max_length=255)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES)
    units_needed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('date', 'hospital_id', 'blood_type')

    def __str__(self):
        return f"{self.date} - {self.hospital_id} needs {self.units_needed} units of {self.blood_type}"
