from django.db import models
from Account.models import Account
from django.utils import timezone


class Notifications(models.Model):
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_user')
    message = models.CharField(default=' ', null=True, max_length=100)
    category = models.CharField(null=True, max_length=14, choices=[
        ('Likes', 'Likes'),
        ('Comments', 'Comments'),
        ('Friendrequests', 'Friendrequests'),
        ('Newfriends', 'Newfriends')
    ])
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.to_user)

    def notify_user(self):
        if Account.allow_notification:
            return self.message
        else:
            if self.category == 'Friendrequests' or self.category == 'Newfriends':
                return self.message

    class Meta:
        ordering = ('-created',)
