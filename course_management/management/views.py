from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from .forms import CourseForm
from django.db.models import Q


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
        if enrolled_count > course.capacity/2:
            course.color = 'yellow'
        elif enrolled_count <= course.capacity / 2:
            course.color = 'green'
        elif enrolled_count == course.capacity:
            course.color = 'red'
        
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
