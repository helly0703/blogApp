from django.urls import path, include
from django.contrib.auth import views as auth_views
from Account import views
from Account.views import (
    HomeView,
    FriendView,
    FriendDetailView,
    ViewFriendDetailView,
    InvitesReceivedView,
    InvitesProfileListView,
    ProfileListView,
    SendInviteView,
    SignUpView,
    RemoveFriendView,
    AcceptInvitesView,
    RejectInvitesView
)
from notifications.views import NotificationsListView

urlpatterns = [
    path('', SignUpView.as_view(), name='register'),
    path('home', HomeView.as_view(), name='home'),  # Takes to the blogs page after login
    path('home/profile/', views.profile, name='profile'),  # Takes to the user profile page
    path('home/friends/', FriendView.as_view(), name='friendspage'),
    path('home/friends/<int:pk>/', FriendDetailView.as_view(), name='friend_detail'),
    path('home/friends/<int:pk>/add', ViewFriendDetailView.as_view(), name='friend_request'),
    path('home/myinvites', InvitesReceivedView.as_view(), name='myinvites'),
    path('home/allprofiles', ProfileListView.as_view(), name='allprofiles'),
    path('home/inviteprofiles', InvitesProfileListView.as_view(), name='inviteprofiles'),
    path('home/sendinvite', SendInviteView.as_view(), name='sendinvite'),
    path('home/removefriend', RemoveFriendView.as_view(), name='removefriend'),
    path('home/acceptrequest', AcceptInvitesView.as_view(), name='acceptrequest'),
    path('home/removerequest', RejectInvitesView.as_view(), name='removerequest'),
    path('home/notifications', NotificationsListView.as_view(), name='notifications'),
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
                                                                   success_url='/'), name='change_password'),
    path('home/blogs/', include('blogs.urls'), name='blogs'),
]
