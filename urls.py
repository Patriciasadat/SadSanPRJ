from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('connections/', views.connections, name='connections'),
    path('admin/', admin.site.urls),
    # Add other URL patterns here
]