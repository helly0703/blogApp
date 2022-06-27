from django.db import models
from PIL import Image
from django.contrib.auth.models import User, AbstractUser
from datetime import date
from django.db.models import Q


class AccountManager(models.Manager):

    def get_all_profiles_to_invites(self, sender):
        profiles = Account.objects.all().exclude(user=sender)
        print(profiles)
        profile = Account.objects.get(user=sender)
        print(profile)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = []
        pending = []
        for rel in qs:
            if rel.status == 'accepted':
                accepted.append(rel.receiver)
                accepted.append(rel.sender)
            elif rel.status == 'send':
                accepted.append(rel.receiver)
                accepted.append(rel.sender)
        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]

        print(available)

        return available

    def get_all_profiles(self, me):
        profiles = Account.objects.all().exclude(user=me)
        return profiles


# Creating Account named model to store user profile details
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default=' ', max_length=50)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    birthday = models.DateField(null=True, default=date(2022, 3, 12))
    gender = models.CharField(null=True,
                              max_length=6,
                              choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')]
                              )
    privacy_mode = models.CharField(null=True, max_length=7, choices=[('PUBLIC', 'PUBLIC'), ('PRIVATE', 'PRIVATE')])
    allow_notification = models.BooleanField(null=True)
    description = models.CharField(default=' ', null=True, max_length=50)
    friendslist = models.ManyToManyField(User, related_name='friendslist', null=True, default=None)

    objects = AccountManager()

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_friends(self):
        return self.friendslist.all()

    def get_friends_no(self):
        return self.friendslist.all().count()

    # def get_all_authors_posts(self):
    #     return self.posts.all()


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)

    objects = RelationshipManager()

    def __str__(self):
        return f'{self.sender}'
