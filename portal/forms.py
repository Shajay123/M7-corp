from django import forms
from .models import User

from django import forms
from .models import Events

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'Address', 'Pan_Number', 'Aadhar_Number', 'phone_number', 'from_time', 'to_time']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'Address': forms.TextInput(attrs={'class': 'form-control'}),
            'Pan_Number': forms.TextInput(attrs={'class': 'form-control'}),
            'Aadhar_Number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'from_time': forms.TimeInput(attrs={'class': 'form-control'}),
            'to_time': forms.TimeInput(attrs={'class': 'form-control'}),
        }




class EventsForm(forms.ModelForm):
    EVENT_CHOICES = (
        ('leave', 'Leave'),
        ('permission', 'Permission'),
        ('late checkin', 'Late Checkin'),
        ('force checkout', 'Force Checkout'),
    )

    name = forms.ChoiceField(choices=EVENT_CHOICES)

    class Meta:
        model = Events
        fields = ['name', 'start', 'end']
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
        }