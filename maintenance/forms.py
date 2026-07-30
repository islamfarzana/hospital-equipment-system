from django import forms
from .models import MaintenanceRecord


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = [
            'equipment', 'vendor', 'issue_description', 'maintenance_cost',
            'start_date', 'end_date', 'maintenance_status',
            'calibration_certificate_ref', 'remarks',
        ]
        widgets = {
            'equipment': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'vendor': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'issue_description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
            'maintenance_cost': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
            'start_date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'maintenance_status': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'calibration_certificate_ref': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'remarks': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 2}),
        }