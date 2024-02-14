from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Deposit, Withdrawal, RecentTransaction
from .mails import send_deposit_verified, send_Withdrawal_verified


@receiver(post_save, sender=Deposit)
def verify_deposit(sender, instance, created, **kwargs):

    if instance.pk is not None:
         
        if instance.verified == True:
            
            # create the user and deposit instance
            user = instance.user
            user.balance += instance.amount
            user.save()
            send_deposit_verified(user=user, deposit=instance)

            # create a recent transacttion
            recent_transactions = RecentTransaction.objects.create(user=user, name="Deposit", amount=instance.amount)
            recent_transactions.save()


@receiver(post_save, sender=Withdrawal)
def verify_withdrawal(sender, instance, created, **kwargs):

    if instance.pk is not None:
         
        if instance.verified == True:

            # create the user and withdrawal instance
            user = instance.user
            user.balance -= instance.amount
            user.save()
            send_Withdrawal_verified(user=user, withdrawal=instance)

            # create a recent transacttion
            recent_transactions = RecentTransaction.objects.create(user=user, name="Withdrawal", amount=instance.amount)
            recent_transactions.save()

