from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


class ChatHomeView(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            return render(request, 'chat/start-chat.html')
