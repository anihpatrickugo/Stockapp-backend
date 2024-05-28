from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Deposit, Withdrawal, RecentTransaction
from .mails import send_deposit_verified, send_Withdrawal_verified, send_deposit_request, send_withdrawal_request


@receiver(post_save, sender=Deposit)
def verify_deposit(sender, instance, created, **kwargs):

    if instance.pk is not None:
         
        if instance.verified == True:
            
            # create the user and deposit instance
            user = instance.user
            user.balance += instance.amount
            user.save()

            try:
                send_deposit_verified(user=user, deposit=instance)
            except Exception as e:
                pass

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

            try:
                send_Withdrawal_verified(user=user, withdrawal=instance)
            except Exception as e:
                pass

            # create a recent transacttion
            recent_transactions = RecentTransaction.objects.create(user=user, name="Withdrawal", amount=instance.amount)
            recent_transactions.save()


"""
This signals are sent when a new deposits or withdrawals are created
"""

@receiver(pre_save, sender=Deposit)
def new_deposit(sender, instance, **kwargs):
    # send an email if a new deposit is created


    if instance.pk is None:

        try:
            send_deposit_request(user=instance.user, deposit=instance)
        except Exception as e:
            pass


@receiver(pre_save, sender=Withdrawal)
def new_withdrawal(sender, instance, **kwargs):
    # send an email if a new withdrawal is created

    if instance.pk is None:
        try:
            send_withdrawal_request(user=instance.user, withdrawal=instance)
        except Exception as e:
            pass
