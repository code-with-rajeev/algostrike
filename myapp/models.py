# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import uuid

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    fund_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    total_return = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    api_secret = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(default=now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.username

class Algo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.CharField(max_length=20, choices=[  # status of Algo 
        ('active', 'Active'), # Live 
        ('inactive', 'Inactive'), # Temporary off
        ('disabled', 'Disabled') # Permanently disabled / under maintainance
    ], default='active')
    subscription_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    min_required_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    max_risk = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank = True) # Percentage
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank = True) # Percentage

    def __str__(self):
        return self.name

# Separate Demo-Trade Log for performance of the Algorithm
class AlgoTradeLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    algo = models.ForeignKey(Algo, on_delete=models.CASCADE)  # Foreign key to identify which algo this log is for
    trade_timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of trade execution
    trade_type = models.CharField(max_length=10, choices=[  # Type of trade
        ('buy', 'Buy'),
        ('sell', 'Sell')
    ])
    quantity = models.IntegerField()  # Number of units traded
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at which trade occurred
    profit_loss = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Profit or loss from trade
    trade_status = models.CharField(max_length=50)  # Completed/Failed/Pending etc.
    additional_info = models.JSONField(blank=True, null=True)  # Optional field for additional data
    
    def __str__(self):
        return f"Algo {self.algo.name} Trade Log {self.id} at {self.trade_timestamp}"

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Links to CustomUser
    algo = models.ForeignKey(Algo, on_delete=models.CASCADE)  # Links to Algo
    subscription_date = models.DateTimeField(auto_now_add=True)  # When the subscription was created
    expiry_date = models.DateTimeField()  # When the subscription will expire
    status = models.CharField(max_length=20, choices=[  # Status of subscription
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled')
    ], default='active')
    subscription_fee = models.DecimalField(max_digits=10, decimal_places=2)  # Fee paid for subscription
    additional_info = models.JSONField(blank=True, null=True)  # Any additional subscription-related data
    
    def __str__(self):
        return f"{self.user.username} subscribed to {self.algo.name}"

    def is_active(self):
        """
        Utility method to check if the subscription is active.
        """
        return self.status == 'active' and self.expiry_date > timezone.now()
        """
        Subscription Renewal
        
        subscription.expiry_date += timedelta(days=30)  # Add 30 days to the expiry
        subscription.save()
        """



class TradeLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name="tradelogs")  # Link to the user
    algo = models.ForeignKey(Algo, on_delete=models.CASCADE)  # Link to the algorithm
    timestamp = models.DateTimeField(auto_now_add=True)  # When the trade was executed
    trade_type = models.CharField(max_length=10, choices=[  # Type of trade
        ('buy', 'Buy'),
        ('sell', 'Sell')
    ])
    trade_status = models.CharField(max_length=10, choices=[  # Type of trade
        ('open', 'Open'),
        ('close', 'Close')
    ], default='open')
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)  # Entry price of the trade
    exit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Exit price, if applicable
    quantity = models.IntegerField()  # Number of units traded
    pnl = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Profit or Loss from the trade
    strategy_notes = models.TextField(blank=True, null=True)  # Optional notes about the trade (e.g., strategy used)
    additional_info = models.JSONField(blank=True, null=True)  # Additional trade-related information

    def __str__(self):
        return f"Trade by {self.user.username} on {self.algo.name} at {self.timestamp}"

    def calculate_pnl(self):
        """
        Utility method to calculate P&L if not already provided.
        """        
        if self.exit_price is not None:
            self.pnl = (self.exit_price - self.entry_price) * self.quantity if self.trade_type == 'buy' else \
                       (self.entry_price - self.exit_price) * self.quantity
            self.save()

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('subscription', 'Subscription'),
        ('refund', 'Refund'),
        ('purchase', 'Purchase'),
        ('cancel', 'Cancellation'),
    ]

    TRANSACTION_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="transactions")
    algo = models.ForeignKey(Algo, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")  # Nullable for non-algo-specific transactions
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)  # Amount charged for the transaction
    transaction_status = models.CharField(max_length=15, choices=TRANSACTION_STATUS, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)  # When the user requested the transaction
    completion_date = models.DateTimeField(null=True, blank=True)  # When the transaction was completed
    description = models.TextField(null=True, blank=True)  # Optional: Additional details

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount} - {self.transaction_status}"
