from django import forms
from .models import StaffRequest


class StaffRequestForm(forms.ModelForm):
    class Meta:
        model = StaffRequest
        fields = ['request_type', 'equipment_category', 'equipment', 'description']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'equipment_category': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'equipment': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 4}),
        }


class StaffRequestReviewForm(forms.ModelForm):
    class Meta:
        model = StaffRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }