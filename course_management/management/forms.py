from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'units', 'department', 'instructor', 'capacity', 'start_time', 'end_time', 'exam_datetime','days']
    
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(required= False ,widget=forms.TimeInput(attrs={'type': 'time'}))
    exam_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    days = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g., Mon, Wed, Fri'}))
