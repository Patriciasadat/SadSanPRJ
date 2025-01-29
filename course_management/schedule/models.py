from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    day_of_week = models.CharField(max_length=10)  # e.g., 'Monday'
    start_time = models.TimeField()
    end_time = models.TimeField()
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
