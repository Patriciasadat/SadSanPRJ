# schedule/urls.py
from django.urls import path
from . import views

app_name = 'schedule'  # Add this line to define the namespace

urlpatterns = [
    path('schedule/', views.weekly_schedule, name='weekly_schedule'),
]
