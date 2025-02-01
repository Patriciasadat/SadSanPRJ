from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    units = models.IntegerField(choices=[(i, str(i)) for i in range(5)])  # 0-4 units
    department = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    days = models.CharField(max_length=50)  # Format like "Mon, Wed, Fri"

    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)  # Make end_time nullable

    exam_datetime = models.DateTimeField()  # DateTime of the final exam

    student = models.ForeignKey('registration.CustomUser', on_delete=models.CASCADE, related_name='management_courses', null=True)

    # New fields for capacity
    capacity = models.PositiveIntegerField(default=40)  # Default to 40 students
    enrolled_students = models.ManyToManyField('registration.CustomUser', related_name='enrolled_courses', blank=True)

    @property
    def remaining_capacity(self):
        return self.capacity - self.enrolled_students.count()

    def save(self, *args, **kwargs):
        if not self.end_time:  # Only set end_time if it is not already set
            start_datetime = datetime.combine(datetime.min, self.start_time)
            self.end_time = (start_datetime + timedelta(hours=1 , minutes=20)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"
