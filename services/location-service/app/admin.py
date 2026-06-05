from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location_type', 'is_active', 'created_at')
    list_filter = ('location_type', 'is_active', 'created_at')
    search_fields = ('name', 'address')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'address', 'location_type')
        }),
        ('Coordinates', {
            'fields': ('latitude', 'longitude', 'point')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
