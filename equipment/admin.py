from django.contrib import admin
from .models import EquipmentCategory, Brand, Vendor, Equipment, EquipmentAuditLog

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description')
    search_fields = ('category_name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name',)
    search_fields = ('brand_name',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'contact_person', 'phone', 'status')
    list_filter = ('status',)
    search_fields = ('vendor_name', 'contact_person')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'equipment_code', 'equipment_name', 'equipment_type',
        'category', 'brand', 'current_status', 'next_calibration_due',
    )
    list_filter = ('current_status', 'equipment_type', 'category', 'brand')
    search_fields = ('equipment_code', 'equipment_name', 'serial_number')
    readonly_fields = ('equipment_code',)


@admin.register(EquipmentAuditLog)
class EquipmentAuditLogAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'action', 'performed_by', 'created_at')
    list_filter = ('action',)
    search_fields = ('equipment__equipment_code', 'action')
    autocomplete_fields = ('equipment', 'performed_by')