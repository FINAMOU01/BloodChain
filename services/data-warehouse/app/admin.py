from django.contrib import admin
from .models import DonationStat, HospitalDemand

@admin.register(DonationStat)
class DonationStatAdmin(admin.ModelAdmin):
    list_display = ('date', 'blood_type', 'region', 'total_donations', 'created_at')
    list_filter = ('date', 'blood_type', 'region')
    search_fields = ('region', 'blood_type')
    readonly_fields = ('created_at',)


@admin.register(HospitalDemand)
class HospitalDemandAdmin(admin.ModelAdmin):
    list_display = ('date', 'hospital_id', 'blood_type', 'units_needed', 'created_at')
    list_filter = ('date', 'blood_type', 'hospital_id')
    search_fields = ('hospital_id', 'blood_type')
    readonly_fields = ('created_at',)
