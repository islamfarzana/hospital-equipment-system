from django import forms
from .models import EquipmentAllocation


class EquipmentAllocationForm(forms.ModelForm):
    class Meta:
        model = EquipmentAllocation
        fields = [
            'equipment', 'ward', 'allocated_by', 'allocated_date',
            'expected_return_date', 'returned_date', 'return_condition',
            'status', 'remarks',
        ]
        widgets = {
            'equipment': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'ward': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'allocated_by': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'allocated_date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'expected_return_date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'returned_date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'return_condition': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'status': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'remarks': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        instance = EquipmentAllocation(**{
            **{k: v for k, v in cleaned_data.items()},
        })
        instance.pk = self.instance.pk
        try:
            instance.clean()
        except forms.ValidationError as e:
            raise forms.ValidationError(e.message)
        return cleaned_data