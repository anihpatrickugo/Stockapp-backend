from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.validators import MinValueValidator
from django.conf import settings


User = get_user_model()

# Create your models here.

class RecentTransaction(models.Model):
    user   =  models.ForeignKey(User, on_delete=models.CASCADE)
    name   =  models.CharField(max_length=30)
    amount =  models.IntegerField()
    logo   =  models.ImageField(blank=True, null=True, upload_to='images/transactions')
    date   =  models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.name} Transaction of ${self.amount}"


class Deposit(models.Model):
    user             =   models.ForeignKey(User, on_delete=models.CASCADE)
    amount           =   models.IntegerField(default=0, validators=[MinValueValidator(settings.SITE_MINIMUM_DEPOSIT_AMAOUNT)])
    trnx_hash        =   models.CharField(max_length=300)
    verified         =   models.BooleanField(default=False)
    date             =   models.DateTimeField(auto_now_add=True)
    reference        =   models.CharField(max_length=10, default=get_random_string(length=10))
    


    def __str__(self):
        return f"{self.user} deposit of ${self.amount}"



class Withdrawal(models.Model):
    user             =   models.ForeignKey(User, on_delete=models.CASCADE)
    amount           =   models.IntegerField(default=0, validators=[MinValueValidator(settings.SITE_MINIMUM_WITHDRAWAL_AMAOUNT)])
    verified         =   models.BooleanField(default=False)  
    date             =   models.DateTimeField(auto_now_add=True)
    reference        =   models.CharField(max_length=10, default=get_random_string(length=10))
    


    def __str__(self):
        return f"{self.user} withdrawal of ${self.amount}"

