from django.contrib import admin
from .models import MaintenanceRecord


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = (
        'equipment', 'vendor', 'maintenance_status',
        'start_date', 'end_date', 'maintenance_cost',
    )
    list_filter = ('maintenance_status', 'vendor')
    search_fields = ('equipment__equipment_code', 'equipment__equipment_name', 'issue_description')
    autocomplete_fields = ('equipment', 'vendor')