from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic import ListView

from notifications.models import Notifications


class NotificationsListView(LoginRequiredMixin,ListView):
    model = Notifications
    template_name = 'Notifications/notifications.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Notifications.objects.filter(to_user=self.request.user.account)
        return qs
