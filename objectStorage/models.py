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


class User(models.Model):
    userName = models.CharField(
        max_length=100, unique=True, blank=False, validators=[validate_english_username, MinLengthValidator(4)]
    )
    email = models.EmailField(
        max_length=100, unique=True, blank=False, validators=[custom_email_validator]
    )
    password = models.CharField(
        max_length=100, blank=False, validators=[MinLengthValidator(6)]
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('userName'),
                name='unique_lower_username'
            )
        ]

    def save(self, *args, **kwargs):
        self.userName = self.userName.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.userName  # Adjust if your __str__ method is different
