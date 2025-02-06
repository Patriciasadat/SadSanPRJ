from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Course, CustomUser
from django.urls import reverse
from datetime import datetime, timedelta
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Course

@login_required
def main_page(request):
    """ Main page for students to view available courses and enroll """
    search_query = request.GET.get('search', '')

    if search_query:
        courses = Course.objects.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(instructor__icontains=search_query)
        )
    else:
        courses = Course.objects.all()

    # Calculate enrollment progress and assign colors
    for course in courses:
        enrolled_count = course.enrolled_students.count()
        percentage = (enrolled_count / course.capacity) * 100 if course.capacity else 0  # Avoid division by zero
        
        if enrolled_count > course.capacity/2:
            course.color = 'yellow'
        elif enrolled_count <= course.capacity / 2:
            course.color = 'green'
        elif enrolled_count == course.capacity:
            course.color = 'red'
        
        course.percentage = percentage

    # Get the current user's enrolled courses
    user = request.user
    enrolled_courses = user.enrolled_courses.all()

    # Return the page with modal-ready data
    return render(request, 'main/main_page.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses,
        'search_query': search_query
    })


@login_required
def enroll_in_course(request, course_code):
    """ Enroll the current user in a course via a modal submission """
    course = get_object_or_404(Course, code=course_code)
    user = request.user

    # Ensure only students (not admins) can enroll
    if user.is_admin:
        messages.error(request, "Admins cannot enroll in courses.")
        return redirect('main:main_page')

    # Check if the course is full
    if course.enrolled_students.count() >= course.capacity:
        messages.error(request, "This course is already full.")
        return redirect('main:main_page')

    # Calculate the total enrolled units
    total_units = sum(enrolled_course.units for enrolled_course in user.enrolled_courses.all())

    # Check if adding this course would exceed max_units
    if total_units + course.units > user.max_units:
        messages.error(request, f"Enrolling in {course.name} would exceed your maximum allowed units ({user.max_units}).")
        return redirect('main:main_page')

    # Check if already enrolled
    if course in user.enrolled_courses.all():
        messages.warning(request, "You are already enrolled in this course.")
        return redirect('main:main_page')

    # Check for overlapping courses or exams
    conflicting_courses = user.enrolled_courses.all()
    for enrolled_course in conflicting_courses:
        if is_course_time_conflict(course, enrolled_course):
            messages.error(request, f"You cannot enroll in {course.name} because it conflicts with {enrolled_course.name}.")
            return redirect('main:main_page')

        if is_exam_conflict(course, enrolled_course):
            messages.error(request, f"You cannot enroll in {course.name} because its exam conflicts with {enrolled_course.name}'s exam.")
            return redirect('main:main_page')

    # Enroll the user in the course
    course.enrolled_students.add(user)
    user.enrolled_courses.add(course)

    # Save changes
    user.save()
    course.save()

    messages.success(request, f"Successfully enrolled in {course.name}!")

    # Redirect back to the main page while preserving the search query
    search_query = request.GET.get('search', '')
    return redirect(f'{reverse("main:main_page")}?search={search_query}')


def is_course_time_conflict(course1, course2):
    """ Checks if the class times of two courses overlap """
    # Ensure courses are on the same days
    if not any(day in course1.days.split(", ") for day in course2.days.split(", ")):
        return False

    # Convert times to datetime for comparison
    start1 = datetime.combine(datetime.min, course1.start_time)
    end1 = start1 + timedelta(hours=1, minutes=20)  # Default duration of 1 hour 20 minutes
    start2 = datetime.combine(datetime.min, course2.start_time)
    end2 = start2 + timedelta(hours=1, minutes=20)

    # Check for overlap
    return (start1 < end2 and start2 < end1)


def is_exam_conflict(course1, course2):
    """ Checks if the final exams of two courses overlap """
    # Compare exam datetimes directly without make_aware
    return course1.exam_datetime == course2.exam_datetime

@login_required
def drop_course(request, course_code):
    """ Drop a course for the current user """
    course = get_object_or_404(Course, code=course_code)
    user = request.user

    # Ensure the user is enrolled in the course
    if course not in user.enrolled_courses.all():
        messages.warning(request, "You are not enrolled in this course.")
        return redirect('main:main_page')

    # Drop the course by removing the user from the enrolled_students list
    course.enrolled_students.remove(user)
    user.enrolled_courses.remove(course)  # This will remove the course from the user's courses

    # Save changes to both user and course
    user.save()
    course.save()

    messages.success(request, f"Successfully dropped {course.name}.")

    # Redirect back to the main page with the search query intact (so it maintains state)
    search_query = request.GET.get('search', '')  # Get the current search query
    return redirect(f'{reverse("main:main_page")}?search={search_query}')

@login_required
def update_profile(request):
    """ Handle profile update via a modal """
    user = request.user

    if request.method == 'POST':
        # Directly update user fields from request.POST
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone', user.phone_number)  # This is your custom field

        # You can add any other fields you want to update here (e.g., student_id)
        
        try:
            user.save()  # Save the updated user
            messages.success(request, "Your profile has been updated!")  # Success message
        except Exception as e:
            messages.error(request, f"There was an error updating your profile: {e}")  # Error message

        return redirect('main:main_page')  # Redirect to the main page after updating

    return redirect('main:main_page')  # If not a POST request, just redirect
