from django.db import models

class Notification(models.Model):
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

    recipient_email = models.EmailField()
    message = models.TextField()
    blood_type_needed = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES)
    hospital_name = models.CharField(max_length=150)
    is_emergency = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient_email} - {self.blood_type_needed}"
