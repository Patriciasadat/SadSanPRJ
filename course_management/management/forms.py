from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'units', 'department', 'instructor', 'days', 'start_time', 'end_time', 'exam_datetime']
    
    # Exclude the student field from the form
    # student = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_student=True), required=False) # optional, if you want to allow selecting a student explicitly
