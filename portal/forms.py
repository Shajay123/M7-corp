from django import forms
from .models import User

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'Address', 'Pan_Number', 'Aadhar_Number', 'Phone_Number', 'from_time', 'to_time']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'Address': forms.TextInput(attrs={'class': 'form-control'}),
            'Pan_Number': forms.TextInput(attrs={'class': 'form-control'}),
            'Aadhar_Number': forms.TextInput(attrs={'class': 'form-control'}),
            'Phone_Number': forms.TextInput(attrs={'class': 'form-control'}),
            'from_time': forms.TimeInput(attrs={'class': 'form-control'}),
            'to_time': forms.TimeInput(attrs={'class': 'form-control'}),
        }