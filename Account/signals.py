from django.db.models import Q
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Account, Relationship
from chat.models import Thread
from notifications.models import Notifications


# To create account instance
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


#  To add birthdate details upon account creation
def update_profile(sender, birthdate, username, **kwargs):
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user)
    account.birthday = birthdate
    account.save()


# To save account instance
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.account.save()


# To update friendslist upon friend request accepted
@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friendslist.add(receiver_.user)
        receiver_.friendslist.add(sender_.user)
        # To create notifications
        sender_message = f'You and {receiver_.user.account} are now friends'
        receiver_message = f'You and {sender_.user.account} are now friends'

        sender_notify = Notifications.objects.create(to_user=sender_.user.account, category='Newfriends',
                                                     message=sender_message)
        receiver_notify = Notifications.objects.create(to_user=receiver_.user.account, category='Newfriends',
                                                       message=receiver_message)
        try:
            existing_thread = Thread.objects.get(
                Q(first_person=sender_.user, second_person=receiver_.user) | Q(first_person=receiver_.user,
                                                                               second_person=sender_.user))
            if existing_thread:
                existing_thread.user_blocked = False
                existing_thread.save()
        except Exception as e:
            create_thread = Thread.objects.create(first_person=sender_.user, second_person=receiver_.user)

            create_thread.save()
        sender_notify.save()
        receiver_notify.save()
        sender_.save()
        receiver_.save()


# To update friendslist upon friend request accepted
@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.friendslist.remove(receiver.user)
    receiver.friendslist.remove(sender.user)
    sender.save()
    receiver.save()
