from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Designation, Staff


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    search_fields = ('username', 'email')


admin.site.register(User, CustomUserAdmin)


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('designation_name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('designation_name',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_code', 'first_name', 'last_name', 'ward', 'designation', 'status', 'joining_date')
    list_filter = ('status', 'ward', 'designation')
    search_fields = ('staff_code', 'first_name', 'last_name', 'email')
admin.site.site_header = "Hospital Equipment Management System"
admin.site.site_title = "HEMS Admin"
admin.site.index_title = "Welcome to HEMS Administration"