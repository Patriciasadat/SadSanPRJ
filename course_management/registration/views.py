from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import CustomUserForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("registration:login")  # Correct redirect
    else:
        form = CustomUserForm()
    
    return render(request, "register.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = "registration/login.html"  # Correct path to the template
