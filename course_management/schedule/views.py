from django.shortcuts import render
from .models import Course

def weekly_schedule(request):
    student_courses = Course.objects.filter(student=request.user)
    schedule = {}
    for course in student_courses:
        if course.day_of_week not in schedule:
            schedule[course.day_of_week] = []
        schedule[course.day_of_week].append(course)
    return render(request, 'schedule/weekly_schedule.html', {'schedule': schedule})
