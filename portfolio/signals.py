from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Position
from transactions.models import  RecentTransaction


@receiver(post_save, sender=Position)
def create_position_transaction(sender, instance, created, **kwargs):
    if instance.pk is not None:

        # subtract user balance instance
        user = instance.user
        user.balance -= instance.price
        user.save()

        # create a recent transacttion
        recent_transactions = RecentTransaction.objects.create(user=user,
                                                               name=instance.stock.name,
                                                               amount=instance.price,
                                                               logo=instance.stock.image
                                                               )
        recent_transactions.save()


