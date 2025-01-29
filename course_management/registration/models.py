from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    national_id = models.CharField(max_length=20, unique=True)
    student_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    is_admin = models.BooleanField(default=False)
    admin_code = models.CharField(max_length=20, blank=True, null=True, unique=True)

    admission_year = models.CharField(max_length=4, blank=True, null=True)
    max_units = models.IntegerField(default=24)

    # Many-to-Many relationship: A student can have multiple courses, and a course can have multiple students.
    courses = models.ManyToManyField("management.Course", related_name="students", blank=True)

    # Fix group & permissions conflict with AbstractUser
    groups = models.ManyToManyField("auth.Group", related_name="+", blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name="+", blank=True)

    def save(self, *args, **kwargs):
        if self.is_admin:
            if not self.admin_code:
                raise ValueError("Admins must provide an admin code!")
            self.username = self.admin_code
            self.student_id = None
            self.admission_year = None
        else:
            if self.student_id:
                if len(self.student_id) == 9:
                    self.admission_year = f"1{self.student_id[:3]}"
                elif len(self.student_id) == 8:
                    self.admission_year = f"13{self.student_id[0]}"
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
