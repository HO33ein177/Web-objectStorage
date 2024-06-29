from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class File(models.Model):
    name = models.CharField(max_length=120)
    size = models.IntegerField(validators=[MinLengthValidator(3)])
    icon = models.ImageField(upload_to='icons')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    access_level_choices = {
        'owner': "owner",
        'visitor': "Visitor"
    }
    access_level = models.CharField(choices=access_level_choices, max_length=20, default='visitor')

    privacy_level_choices = {
        'pub': "public",
        'priv': "private",
    }
    privacy_level = models.CharField(choices=privacy_level_choices, max_length=20, default='priv')
