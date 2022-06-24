from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notifications
from .models import Like, Comment,Post


@receiver(post_save, sender=Like)
def like_notification(sender, instance, created, **kwargs):
    from_user = instance.user
    post = instance.post
    post_title = post.title
    notify_user = post.author.account
    if instance.value == 'Unlike':
        msg = f'{from_user} liked your Post "{post_title}"'
        new_like = Notifications.objects.create(to_user=notify_user, category='Likes',
                                     message=msg)
        new_like.save()

@receiver(post_save, sender=Comment)
def like_notification(sender, instance, created, **kwargs):
    from_user = instance.user
    post = instance.post
    notify_user = post.author.account
    post_title = post.title
    comment_text = instance.body
    msg = f'{from_user} commented: "{comment_text}" on your Post "{post_title}"'
    new_like = Notifications.objects.create(to_user=notify_user, category='Likes',
                                     message=msg)
    new_like.save()


@receiver(post_save, sender=Post)
def new_post_notification(sender, instance, created, **kwargs):
    posted_by = instance.author
    notify_users_list = instance.author.account.friendslist
    msg = f'{posted_by} made a new post'
    for user in notify_users_list.all():
        if user.account.allow_notification:
            new_post = Notifications.objects.create(to_user=user.account, category='Likes',
                                     message=msg)
            new_post.save()
