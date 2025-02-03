from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('profile/', views.update_profile, name='update_profile'),
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
]
