from django.urls import path
from Account import views

urlpatterns = [
    path('home/', views.home, name='home'),                     # Takes to the home page after login
    path('home/profile/', views.profile, name='profile'),       # Takes to the user profile page
]

