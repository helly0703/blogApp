from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Q



class AccountManager(models.Manager):

    def get_all_profiles_to_invites(self, sender):
        profiles = Account.objects.all().exclude(user=sender)
        print(profiles)
        profile = Account.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = []
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
                              choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')],
                              )
    privacy_mode = models.CharField(null=True, max_length=7, choices=[('PUBLIC', 'PUBLIC'), ('PRIVATE', 'PRIVATE')],
                                    editable=True,default='PRIVATE')
    allow_notification = models.BooleanField(null=True, editable=True,default=True)
    description = models.CharField(default='',blank=True, null=True, max_length=50)
    friendslist = models.ManyToManyField(User, related_name='friendslist', null=True, default=None, blank=True)
    blockedlist = models.ManyToManyField(User, related_name='blocklist', null=True, default=None, blank=True)


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

    def get_blocklist(self):
        print(self.blockedlist.all())
        return self.blockedlist.all()

    def get_user(self):
        user = User.objects.get(pk=self.user_id)
        print(user)
        return user

    def request_exist(self):
        rel = Relationship.objects.filter(sender=self)
        if rel:
            return rel
        else:
            rel = Relationship.objects.filter(receiver=self)
            return rel

    def get_all_authors_posts(self):
        user = self.get_user()
        from blogs.models import Post
        posts = Post.objects.filter(author=user)
        return posts

    def check_send_request(self):
        qs = Relationship.objects.filter(sender=self,status='send')
        receivers = []
        for obj in qs:
            receivers.append(obj.receiver)
        return receivers

    def check_received_request(self):
        qs = Relationship.objects.filter(receiver=self,status='send')
        senders = []
        for obj in qs:
            senders.append(obj.sender)
        return senders


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
