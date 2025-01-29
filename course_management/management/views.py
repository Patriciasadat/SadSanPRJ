from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from .forms import CourseForm

@login_required
def manage_courses(request):
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to view this page.")
        return redirect('home')

    courses = Course.objects.all()

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully!")
            return redirect('manage_courses')
    else:
        form = CourseForm()

    # Update template path
    return render(request, 'management/manage.html', {'form': form, 'courses': courses})

@login_required
def edit_course(request, course_id):
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to edit courses.")
        return redirect('home')

    course = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=course)

    if form.is_valid():
        form.save()
        messages.success(request, "Course updated successfully!")
        return redirect('manage_courses')

    # Update template path
    return render(request, 'management/edit_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    if not request.user.is_admin:
        messages.error(request, "You don't have permission to delete courses.")
        return redirect('home')

    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect('manage_courses')
