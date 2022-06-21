# Generated by Django 4.0.5 on 2022-06-16 10:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Account', '0006_account_friendslist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='friendslist',
            field=models.ManyToManyField(default=None, null=True, related_name='friendslist', to=settings.AUTH_USER_MODEL),
        ),
    ]
