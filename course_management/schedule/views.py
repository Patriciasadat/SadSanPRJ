from django.shortcuts import render
from management.models import Course  # Adjust the import according to where it's defined

def weekly_schedule(request):
    if not request.user.is_authenticated:
        return render(request, 'schedule.html', {'schedule': {}})

    # Get the courses for the logged-in student
    student_courses = request.user.courses.all()  # Using the related_name from CustomUser model

    # Create an empty schedule dictionary
    schedule = {}

    # Populate the schedule dictionary based on the courses the student is enrolled in
    for course in student_courses:
        for day in course.days.split(", "):  # Assuming days are stored like "Mon, Wed, Fri"
            if day not in schedule:
                schedule[day] = []
            schedule[day].append(course)

    # Sort the days of the week to display them in a consistent order
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    sorted_schedule = {day: schedule.get(day, []) for day in days_of_week}

    # Render the weekly schedule template
    return render(request, 'schedule.html', {'schedule': sorted_schedule})
