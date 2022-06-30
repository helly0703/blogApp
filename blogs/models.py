from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

from Account.models import Account


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField( null=True, default=None, blank=True, upload_to='blog_pics/')
    date_posted = models.DateTimeField(default=timezone.now)
    # category_id = models.ForeignKey(PostCategory, on_delete=models.SET_DEFAULT(None))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.ManyToManyField(Account, blank=True, related_name='likes')
    saved = models.ManyToManyField(Account, blank=True, related_name='saved')

    def __str__(self):
        return self.title

    def num_of_likes(self):
        return self.liked.all().count()

    def num_of_comments(self):
        comments = Comment.objects.all().filter(post=self).count()
        return comments

    def get_comments(self):
        comment_list = Comment.objects.all().filter(post=self)[:5]
        return comment_list

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    class Meta:
        ordering = ('-date_posted',)


class Comment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.pk)


    class Meta:
        ordering = ('-created',)



LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)


class Like(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"


SAVE_CHOICES = (
    ('Save', 'Save'),
    ('Unsave', 'Unsave')
)


class SavePost(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=SAVE_CHOICES, max_length=8)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"






