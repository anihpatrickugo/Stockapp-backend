from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

from .utils import generate_activation_code

from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=100000000000000)
    wallet_address = models.CharField(blank=True, null=True, max_length=50)
    photo = models.ImageField(blank=True, null=True, upload_to='images/profile')
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
         if (self.is_superuser):
            return f'Admin   {self.id}'

         return f'{self.first_name }  {self.last_name}'
    



class ActivationCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=generate_activation_code)


class Notifications(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title       = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
