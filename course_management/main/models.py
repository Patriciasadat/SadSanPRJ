from django.contrib.auth.models import User
from django.db import models

class Course(models.Model):
    """ Represents a course that students can enroll in """
    name = models.CharField(max_length=255, verbose_name="Course Name")
    code = models.CharField(max_length=50, unique=True, verbose_name="Course Code")
    department = models.CharField(max_length=100, verbose_name="Department")
    instructor = models.CharField(max_length=255, verbose_name="Instructor")
    capacity = models.PositiveIntegerField(default=30, verbose_name="Capacity")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def enrolled_students_count(self):
        """ Returns the number of students enrolled in this course """
        return self.enrolled_students.count()

    @property
    def is_full(self):
        """ Checks if the course is full """
        return self.enrolled_students_count >= self.capacity


class Student(models.Model):
    """ Represents a student who can enroll in courses """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    enrolled_courses = models.ManyToManyField(Course, related_name="enrolled_students", blank=True)
    date_of_birth = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number", blank=True, null=True)
    address = models.TextField(verbose_name="Address", blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def enrolled_courses_count(self):
        """ Returns the number of courses the student is enrolled in """
        return self.enrolled_courses.count()
