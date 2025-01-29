from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'units', 'department', 'instructor', 'days', 'time', 'exam_datetime']
