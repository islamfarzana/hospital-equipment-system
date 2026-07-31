from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Staff

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Password',
        })
    )

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'staff_code', 'user', 'ward', 'designation',
            'first_name', 'last_name', 'email', 'phone',
            'joining_date', 'status',
        ]
        widgets = {
            'staff_code': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'user': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'ward': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'designation': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'first_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full'}),
            'phone': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'joining_date': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }