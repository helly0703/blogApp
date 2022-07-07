
from django.urls import path

from .views import ChatHomeView

urlpatterns = [
    path('', ChatHomeView.as_view(), name='start-chat'),
]
