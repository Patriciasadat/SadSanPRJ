from django.db import models
from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    units = models.IntegerField(choices=[(i, str(i)) for i in range(5)])  # 0-4 units
    department = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    days = models.CharField(max_length=50)  # Can store days in a format like "Mon, Wed, Fri"
    time = models.CharField(max_length=50)  # Store time, e.g., "10:00 AM - 12:00 PM"
    exam_datetime = models.DateTimeField()  # DateTime of the final exam

    def __str__(self):
        return self.name

# Create your models here.
