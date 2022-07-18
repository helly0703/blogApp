import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.views import View
from .models import Thread
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class ChatHomeView(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            threads = Thread.objects.by_user(user=self.request.user).prefetch_related('chatmessage_thread')
            print(f"Threads {threads}")
            context = {
                'Threads': threads
            }
            return render(request, 'chat/start-chat.html', context)



@csrf_exempt
def messageViewed(request):
    print("bhjdbsfdn")
    thread_id = request.POST.get('thread_id')
    thread_check = Thread.objects.get(id=thread_id)
    thread_check.new_msg_flag = False
    thread_check.save()
    msg = {
        'Success': 'Success'
    }
    return JsonResponse(msg)
