from django import forms
from .models import User

from django import forms
from .models import Events
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'Address', 'Pan_Number', 'Aadhar_Number', 'phone_number', 'from_time', 'to_time']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'required': True}),
            'Address': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'Pan_Number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'Aadhar_Number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'from_time': forms.TimeInput(attrs={'class': 'form-control', 'required': True}),
            'to_time': forms.TimeInput(attrs={'class': 'form-control', 'required': True}),
        }




class EventsForm(forms.ModelForm):
    EVENT_CHOICES = (
        ('leave', 'Leave'),
        ('permission', 'Permission'),
        ('late checkin', 'Late Checkin'),
        ('force checkout', 'Force Checkout'),
    )

    name = forms.ChoiceField(choices=EVENT_CHOICES, required=True)

    class Meta:
        model = Events
        fields = ['name', 'start', 'end']
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date', 'required': 'required'}),
            'end': forms.DateInput(attrs={'type': 'date', 'required': 'required'}),
        }