from django.shortcuts import render
from .models import Course

def weekly_schedule(request):
    if not request.user.is_authenticated:
        return render(request, 'schedule/weekly_schedule.html', {'schedule': {}})

    # Get the courses for the logged-in student
    student_courses = request.user.courses.all()  # Using the Many-to-Many field

    schedule = {}
    for course in student_courses:
        for day in course.days.split(", "):  # Assuming days are stored like "Mon, Wed, Fri"
            if day not in schedule:
                schedule[day] = []
            schedule[day].append(course)

    return render(request, 'schedule/weekly_schedule.html', {'schedule': schedule})
