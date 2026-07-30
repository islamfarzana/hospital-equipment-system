from django import forms
from .models import Ward


class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ['ward_code', 'ward_name', 'head_of_department', 'status']
        widgets = {
            'ward_code': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'ward_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'head_of_department': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'status': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }