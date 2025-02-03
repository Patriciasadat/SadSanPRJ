from django import forms
from .models import Student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['date_of_birth', 'phone_number', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your address'}),
        }
