from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from datetime import date


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
    privacy_mode = models.CharField(null=True,max_length=7, choices=[('PUBLIC', 'PUBLIC'), ('PRIVATE', 'PRIVATE')])
    allow_notification = models.BooleanField(null=True)
    description = models.CharField(default=' ',null=True,max_length=50)

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
