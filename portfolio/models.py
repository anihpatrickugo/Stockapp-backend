from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    image  = models.ImageField(blank=True, null=True, upload_to='images/ticker')
    open = models.DecimalField(decimal_places=1, max_digits=100000, default=0)
    prev_close = models.DecimalField(decimal_places=1, max_digits=100000, default=0)
    volume = models.IntegerField(default=0)
    market_cap = models.DecimalField(decimal_places=3, max_digits=100000, default=0)

    def __str__(self):
        return self.ticker
    
class Position(models.Model):

    direction_option = (
            ('Long','Long'),
            ('Short','Short')
        )
    
    direction = models.CharField(max_length=200, null=True, choices=direction_option)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    volume = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=100000)
    date   =  models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.stock.ticker} {self.direction} Position for {self.user.first_name} {self.user.last_name}"
    