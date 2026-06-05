from django.db import models

class Reward(models.Model):
    donor_id = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.donor_id} - {self.points} points"


class Redemption(models.Model):
    donor_id = models.CharField(max_length=255)
    reward = models.CharField(max_length=255)
    redeemed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-redeemed_at']

    def __str__(self):
        return f"{self.donor_id} redeemed {self.reward}"
