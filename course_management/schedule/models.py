from django.db import models
from django.conf import settings  # Import settings to reference CustomUser

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    units = models.IntegerField(choices=[(i, str(i)) for i in range(5)])  # 0-4 units
    department = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    days = models.CharField(max_length=50)  # Format like "Mon, Wed, Fri"
    
    # More precise time fields
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    exam_datetime = models.DateTimeField()  # DateTime of the final exam

    # Link to CustomUser instead of Student
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses", null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
