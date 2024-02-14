from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Deposit, Withdrawal
from .mails import send_deposit_verified, send_Withdrawal_verified


@receiver(post_save, sender=Deposit)
def verify_deposit(sender, instance, created, **kwargs):

    if instance.pk is not None:
         
        if instance.verified == True:
         
            user = instance.user
            user.balance += instance.amount
            user.save()
            send_deposit_verified(user=user, deposit=instance)


@receiver(post_save, sender=Withdrawal)
def verify_withdrawal(sender, instance, created, **kwargs):

    if instance.pk is not None:
         
        if instance.verified == True:
            
            user = instance.user
            user.balance -= instance.amount
            user.save()
            send_Withdrawal_verified(user=user, withdrawal=instance)
