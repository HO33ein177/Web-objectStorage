from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .validator import *
from django.core.validators import MinLengthValidator
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.constraints import UniqueConstraint
from django.db.models.functions import Lower


# class User(models.Model):
#     username = models.CharField(
#         max_length=100, unique=True, blank=False, default='h'
#     )
#     email = models.EmailField(
#         max_length=100, unique=True, blank=False
#     )
#     password = models.CharField(
#         max_length=100, blank=False
#     )


