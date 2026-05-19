from django.db import models

class Reward(models.Model):
    donor_email = models.EmailField()
    donor_wallet = models.CharField(max_length=100)
    tokens_minted = models.PositiveIntegerField()
    bag_id = models.CharField(max_length=100)
    tx_hash = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_email} - {self.tokens_minted}"
