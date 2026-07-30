from django import forms
from .models import Equipment, EquipmentCategory, Brand, Vendor


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'category', 'brand', 'vendor', 'equipment_name', 'equipment_type',
            'model', 'serial_number', 'purchase_date', 'purchase_cost',
            'warranty_expiry', 'last_calibration_date', 'next_calibration_due',
            'current_status', 'remarks',
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'brand': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'vendor': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'equipment_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'equipment_type': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'model': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'serial_number': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'purchase_date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'purchase_cost': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
            'warranty_expiry': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'last_calibration_date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'next_calibration_due': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'current_status': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'remarks': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
        }