from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=200)
    contact_email = models.EmailField(unique=True)
    contact_phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class BloodStock(models.Model):
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
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES)
    units_available = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hospital.name} - {self.blood_type}"

class BloodRequest(models.Model):
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
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ]
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES)
    units_needed = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hospital.name} - {self.blood_type} - {self.status}"

