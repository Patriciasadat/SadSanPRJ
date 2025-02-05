from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from management.models import Course
from datetime import datetime

@login_required
def weekly_schedule(request):
    # Get all courses the logged-in user is enrolled in
    user_courses = request.user.enrolled_courses.all()

    # Dictionary to store schedule by day
    schedule = {day: [] for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']}

    for course in user_courses:
        # Ensure 'days' is correctly formatted and split it into a list
        course_days = [day.strip() for day in course.days.split(",")] if course.days else []
        
        for day in course_days:
            if day in schedule:  # Only add valid days
                schedule[day].append({
                    'course': course.name,
                    'code': course.code,
                    'instructor': course.instructor,
                    'start_time': course.start_time.strftime('%H:%M') if course.start_time else 'TBA',
                    'end_time': course.end_time.strftime('%H:%M') if course.end_time else 'TBA',
                })

    # Sort courses by start_time within each day
    for day, courses in schedule.items():
        courses.sort(key=lambda x: datetime.strptime(x['start_time'], '%H:%M') if x['start_time'] != 'TBA' else datetime.max)

    return render(request, 'schedule.html', {'schedule': schedule})
