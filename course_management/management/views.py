from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from .forms import CourseForm
from django.db.models import Q
from datetime import datetime, timedelta
from registration.models import CustomUser 

@login_required
def manage_courses(request):
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('home')

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
    
    
    # Calculate progress and color for each course
    for course in courses:
        enrolled_count = course.enrolled_students.count()
        percentage = (enrolled_count / course.capacity) * 100 if course.capacity else 0  # Avoid division by zero
        if enrolled_count == course.capacity:
            course.color = 'red'
        elif enrolled_count > course.capacity/2:
            course.color = 'yellow'
        else:
            course.color = 'green'
        
        course.percentage = percentage
    
    # Handle the POST request for adding new courses
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)

            # Ensure the capacity is at least 1
            if course.capacity < 1:
                messages.error(request, "Capacity must be at least 1.")
                return redirect('management:manage_courses')

            course.save()
            messages.success(request, "Course added successfully!")
            return redirect('management:manage_courses')

    else:
        form = CourseForm()

    return render(request, 'management/manage.html', {
        'form': form,
        'courses': courses,
        'search_query': search_query
    })


@login_required
def edit_course(request, course_id):
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to edit courses.")
        return redirect('home')

    course = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=course)

    if form.is_valid():
        updated_course = form.save(commit=False)

        # Prevent reducing capacity below the number of enrolled students
        enrolled_students_count = course.enrolled_students.count()
        if updated_course.capacity < enrolled_students_count:
            messages.error(request, f"Cannot set capacity below the {enrolled_students_count} enrolled students.")
            return redirect('management:manage_courses')

        updated_course.save()
        messages.success(request, "Course updated successfully!")
        return redirect('management:manage_courses')

    return render(request, 'management/edit_course.html', {'form': form, 'course': course})


@login_required
def delete_course(request, course_id):
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to delete courses.")
        return redirect('home')

    course = get_object_or_404(Course, id=course_id)

    # Prevent deleting courses with enrolled students
    if course.enrolled_students.exists():
        messages.error(request, "Cannot delete a course with enrolled students. Remove students first.")
        return redirect('management:manage_courses')

    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect('management:manage_courses')


@login_required
def view_students(request, course_id):
    """ View enrolled students for a specific course """
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('home')

    course = get_object_or_404(Course, id=course_id)
    students = course.enrolled_students.all()

    return render(request, 'management/view_students.html', {'course': course, 'students': students})




@login_required
def enroll_student_admin(request, course_id):
    """Enroll a student in a course using their student ID (admin feature)."""
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        course = get_object_or_404(Course, id=course_id)

        # Ensure the user is an admin
        if not request.user.is_admin:
            messages.error(request, "You do not have permission to enroll students.")
            return redirect("management:manage_courses")

        # Retrieve the student based on student_id
        student = CustomUser.objects.filter(student_id=student_id, is_admin=False).first()

        if not student:
            messages.error(request, "No student found with this ID.")
            return redirect("management:manage_courses")

        # Check if the course is full
        if course.enrolled_students.count() >= course.capacity:
            messages.error(request, "This course is already full.")
            return redirect("management:manage_courses")

        # Check if student is already enrolled
        if course in student.enrolled_courses.all():
            messages.warning(request, "This student is already enrolled in this course.")
            return redirect("management:manage_courses")

        # Check for time conflicts with already enrolled courses
        for enrolled_course in student.enrolled_courses.all():
            if is_course_time_conflict(course, enrolled_course):
                messages.error(
                    request,
                    f"Cannot enroll {student.username} in {course.name} due to a time conflict with {enrolled_course.name}."
                )
                return redirect("management:manage_courses")

            if is_exam_conflict(course, enrolled_course):
                messages.error(
                    request,
                    f"Cannot enroll {student.username} in {course.name} due to an exam conflict with {enrolled_course.name}."
                )
                return redirect("management:manage_courses")

        # Add the student to the course
        course.enrolled_students.add(student)

        messages.success(request, f"{student.username} has been enrolled in {course.name}.")
        return redirect("management:manage_courses")

    return redirect("management:manage_courses")



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
