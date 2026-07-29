from django.contrib import admin
from .models import StaffRequest


@admin.register(StaffRequest)
class StaffRequestAdmin(admin.ModelAdmin):
    list_display = (
        'staff', 'request_type', 'equipment', 'status', 'created_at', 'approved_by',
    )
    list_filter = ('status', 'request_type')
    search_fields = ('staff__first_name', 'staff__last_name', 'description')
    autocomplete_fields = ('staff', 'equipment_category', 'equipment', 'approved_by')