from django.contrib import admin
from .models import EquipmentAllocation


@admin.register(EquipmentAllocation)
class EquipmentAllocationAdmin(admin.ModelAdmin):
    list_display = (
        'equipment', 'ward', 'allocated_date',
        'expected_return_date', 'returned_date', 'status', 'allocated_by',
    )
    list_filter = ('status', 'ward')
    search_fields = ('equipment__equipment_code', 'equipment__equipment_name')
    autocomplete_fields = ('equipment', 'ward')