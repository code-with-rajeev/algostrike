# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    pnl = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    invested = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Trade(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Linking to CustomUser
    trade_type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    symbol = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    trade_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trade_type} {self.symbol} - {self.quantity} units at {self.price}"

class TradeLog(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)  # Linking to Trade model
    action = models.CharField(max_length=10, choices=[('entry', 'Entry'), ('exit', 'Exit')])
    price = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} at {self.price} on {self.timestamp}"