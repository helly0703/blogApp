from django.urls import path, include
from django.contrib.auth import views as auth_views
from Account import views
from Account.views import FriendView, FriendDetailView, AddFriendView

urlpatterns = [
    path('', views.register, name='register'),
    path('home', views.home, name='home'),                     # Takes to the blogs page after login
    path('home/profile/', views.profile, name='profile'),       # Takes to the user profile page
    path('home/friends/', FriendView.as_view(), name='friendspage'),
    path('home/friends/<int:pk>/', FriendDetailView.as_view(), name='friend_detail'),
    path('home/friends/<int:pk>/add', AddFriendView.as_view(), name='friend_request'),



    path('accounts/login/', auth_views.LoginView.as_view(template_name='Account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Account/logout.html'), name='logout'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='Account/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='Account/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='Account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='Account/password_reset_complete.html'),
         name='password_reset_complete'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='Account/change-password.html',
                                                                   success_url = '/'),
        name='change_password'
    ),
    path('home/blogs/', include('blogs.urls'), name='blogs'),


]

