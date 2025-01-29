from django.db import models
from django.conf import settings 
from datetime import timedelta

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    units = models.IntegerField(choices=[(i, str(i)) for i in range(5)])  # 0-4 units
    department = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    days = models.CharField(max_length=50)  # Format like "Mon, Wed, Fri"
    
    start_time = models.TimeField()
    end_time = models.TimeField(default=(start_time + timedelta(hours=1)))
    
    exam_datetime = models.DateTimeField()  # DateTime of the final exam

    # Set a unique related_name for this app's course
    student = models.ForeignKey('registration.CustomUser', on_delete=models.CASCADE, related_name='management_courses')

    def __str__(self):
        return f"{self.name} ({self.code})"
