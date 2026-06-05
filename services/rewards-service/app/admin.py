from django.contrib import admin
from .models import Reward, Redemption

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor_id', 'points', 'created_at')
    search_fields = ('donor_id', 'reason')
    readonly_fields = ('created_at',)


@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'donor_id', 'reward', 'redeemed_at')
    search_fields = ('donor_id', 'reward')
    readonly_fields = ('redeemed_at',)
