# registration/urls.py

from django.urls import path
from .views import register
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'registration'  # Add a namespace for this app

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),  # Added logout URL
]
