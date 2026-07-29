from django.contrib import admin
from .models import Ward


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('ward_code', 'ward_name', 'head_of_department', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('ward_code', 'ward_name')