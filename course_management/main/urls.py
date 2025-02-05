# In main/urls.py
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('profile/', views.update_profile, name='update_profile'),
    path('enroll/<str:course_code>/', views.enroll_in_course, name='enroll_in_course'),
    path('drop_course/<str:course_code>/', views.drop_course, name='drop_course'),  # Add this line
]
