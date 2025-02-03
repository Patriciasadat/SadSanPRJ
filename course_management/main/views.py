from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Student
from .forms import StudentProfileForm


@login_required
def main_page(request):
    """ Main page for students to view available courses and enroll """
    # Get the search query from the GET request (if it exists)
    search_query = request.GET.get('search', '')

    # Filter courses based on the search query (if provided)
    if search_query:
        courses = Course.objects.filter(
            Q(name__icontains=search_query) |  # Search by course name
            Q(code__icontains=search_query) |  # Search by course code
            Q(department__icontains=search_query) |  # Search by department
            Q(instructor__icontains=search_query)  # Search by instructor name
        )
    else:
        courses = Course.objects.all()

    # Calculate enrollment progress for each course
    for course in courses:
        enrolled_count = course.enrolled_students.count()
        percentage = (enrolled_count / course.capacity) * 100 if course.capacity else 0  # Avoid division by zero
        if enrolled_count >= course.capacity:
            course.color = 'green'
        elif enrolled_count >= course.capacity / 2:
            course.color = 'yellow'
        else:
            course.color = 'red'
        
        course.percentage = percentage

    # Get the current student's enrolled courses
    student = request.user.student
    enrolled_courses = student.enrolled_courses.all()

    return render(request, 'students/main_page.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses,
        'search_query': search_query
    })


@login_required
def enroll_in_course(request, course_id):
    """ Enroll the current student in a course """
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student

    # Check if the course is already full
    if course.enrolled_students.count() >= course.capacity:
        messages.error(request, "This course is already full.")
        return redirect('students:main_page')

    # Check if the student is already enrolled in the course
    if course in student.enrolled_courses.all():
        messages.warning(request, "You are already enrolled in this course.")
        return redirect('students:main_page')

    # Enroll the student in the course
    course.enrolled_students.add(student)
    messages.success(request, f"Successfully enrolled in {course.name}!")
    return redirect('students:main_page')


@login_required
def drop_course(request, course_id):
    """ Drop a course for the current student """
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student

    # Check if the student is enrolled in the course
    if course not in student.enrolled_courses.all():
        messages.warning(request, "You are not enrolled in this course.")
        return redirect('students:main_page')

    # Drop the course
    course.enrolled_students.remove(student)
    messages.success(request, f"Successfully dropped {course.name}.")
    return redirect('students:main_page')


@login_required
def view_profile(request):
    """ View and update the student's profile """
    student = request.user.student

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('students:view_profile')
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'students/view_profile.html', {'form': form})

@login_required
def update_profile(request):
    student = request.user.student  # Get the current student

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('main:update_profile')
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'main/update_profile.html', {'form': form})
    
@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student

    # Check if the course is already full
    if course.enrolled_students.count() >= course.capacity:
        messages.error(request, "This course is already full.")
        return redirect('main:main_page')

    # Check if the student is already enrolled in the course
    if course in student.enrolled_courses.all():
        messages.warning(request, "You are already enrolled in this course.")
        return redirect('main:main_page')

    # Enroll the student in the course
    course.enrolled_students.add(student)
    messages.success(request, f"Successfully enrolled in {course.name}!")
    return redirect('main:main_page')
