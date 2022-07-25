from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from notifications.models import Notifications


class NotificationsListView(LoginRequiredMixin, ListView):
    """
    Returns all the notification of logged in user
    """
    model = Notifications
    template_name = 'Notifications/notifications.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Notifications.objects.filter(to_user=self.request.user.account)
        return qs
