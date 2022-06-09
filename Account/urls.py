from django.urls import path, include
from Account import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='Account/login.html'), name='login'),
    path('', views.register, name='register'),
    path('login/home/', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Account/logout.html'), name='logout'),

]

