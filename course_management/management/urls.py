from django.urls import path
from . import views

app_name = 'management'  # This sets the namespace for this app

urlpatterns = [
    path('manage/', views.manage_courses, name='manage_courses'),
    path('edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete/<int:course_id>/', views.delete_course, name='delete_course'),
]
