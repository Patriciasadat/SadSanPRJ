from django import forms
from .models import CustomUser

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Changed from Student to CustomUser
        fields = ['phone_number', 'national_id', 'student_id', 'admission_year']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
            'national_id': forms.TextInput(attrs={'placeholder': 'Enter your national ID'}),
            'student_id': forms.TextInput(attrs={'placeholder': 'Enter your student ID'}),
            'admission_year': forms.TextInput(attrs={'readonly': 'readonly'}),  # Set as readonly if auto-generated
        }
