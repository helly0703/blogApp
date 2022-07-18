
from django.urls import path

from .views import ChatHomeView, messageViewed

urlpatterns = [
    path('', ChatHomeView.as_view(), name='start-chat'),
    path('view-msg/', messageViewed, name='msg-viewed'),

]
