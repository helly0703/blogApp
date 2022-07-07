from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from .models import Thread


class ChatHomeView(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            threads = Thread.objects.by_user(user=self.request.user).prefetch_related('chatmessage_thread')
            context = {
                'Threads': threads
            }
            return render(request, 'chat/start-chat.html',context)
