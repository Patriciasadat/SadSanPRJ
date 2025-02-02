from django import forms
from .models import Course
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class CourseForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'})
    )
    code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Code'})
    )
    units = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Units', 
            'min': '0',  # Set minimum value to 0
            'max': '4',  # Set maximum value to 4
            'step': '1'  # Ensures that only integer values are selected
        }),
        validators=[MinValueValidator(0), MaxValueValidator(4)]
    )
    department = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'})
    )
    instructor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instructor Name'})
    )
    capacity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacity' ,
                                        'min': '0', 'step' : '1'})
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    end_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    exam_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    days = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mon, Wed, Fri'})
    )

    class Meta:
        model = Course
        fields = ['name', 'code', 'units', 'department', 'instructor', 'capacity', 'start_time', 'end_time', 'exam_datetime', 'days']

    # Custom clean method to validate that end_time is later than start_time
    def clean(self):
        cleaned_data = super().clean()
        
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Ensure that end_time is later than start_time if both are provided
        if start_time and end_time:
            if end_time <= start_time:
                raise ValidationError("End time must be later than start time.")
        
        return cleaned_data
