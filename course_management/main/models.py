# main/models.py
from django.contrib.auth.models import User
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    instructor = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(default=30)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def enrolled_students_count(self):
        return self.enrolled_students.count()

    @property
    def is_full(self):
        return self.enrolled_students_count >= self.capacity


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    enrolled_courses = models.ManyToManyField(Course, related_name="enrolled_students", blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def enrolled_courses_count(self):
        return self.enrolled_courses.count()
