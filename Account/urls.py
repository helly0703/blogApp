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
    RejectInvitesView,
    SearchProfileView,
    SettingsFormView,
    BlockUserCreateView,
    MyBlogsView,
)
from notifications.views import NotificationsListView

urlpatterns = [
    path('', SignUpView.as_view(), name='register'),
    path('home', HomeView.as_view(), name='home'),  # Takes to the blogs page after login
    path('home/profile/', views.profile, name='profile'),  # Takes to the user profile page
    path('home/profile/settings', SettingsFormView.as_view(), name='settings'),  # Takes to the user profile page
    path('home/friends/', FriendView.as_view(), name='friends_page'),
    path('home/friends/<int:pk>/', FriendDetailView.as_view(), name='friend_detail'),
    path('home/friends/<int:pk>/add', ViewFriendDetailView.as_view(), name='friend_request'),
    path('home/my-invites', InvitesReceivedView.as_view(), name='my_invites'),
    path('home/all-profiles', ProfileListView.as_view(), name='all_profiles'),
    path('home/search-profile', SearchProfileView.as_view(), name='search_profile'),
    path('home/block-profile', BlockUserCreateView.as_view(), name='block_profile'),
    path('home/invite-profiles', InvitesProfileListView.as_view(), name='invite_profiles'),
    path('home/send-invite', SendInviteView.as_view(), name='send_invite'),
    path('home/remove-friend', RemoveFriendView.as_view(), name='remove_friend'),
    path('home/my-blogs', MyBlogsView.as_view(), name='my_blogs'),


    path('home/accept-request', AcceptInvitesView.as_view(), name='accept_request'),
    path('home/remove-request', RejectInvitesView.as_view(), name='remove_request'),
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
