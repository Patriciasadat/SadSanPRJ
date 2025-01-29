from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('schedule/', views.weekly_schedule, name='weekly_schedule'),  # URL for the schedule page
]
