# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import uuid

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    fund_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0) # Wallet balance
    date_joined = models.DateTimeField(default=now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    active_plan_details = models.JSONField(
        default=dict(
            activePlan={},  # {"planID": planID, "name": planName}
            expiredPlan={}  # Recently expired plan
        )
    )
    preference = models.JSONField(
        default=dict(theme="Light", notification="Yes")
    )
    profile_information = models.JSONField(
        default=dict(
            tradingExperience="",
            interestedProduct="",
            codingExperience="",
            tradingGoal=""
        )
    )
    strategy_information = models.JSONField(
        default=dict(
            strategiesSaved=0, # created / customized by user 
            runningStrategies=0,
            analyticAccess="OFF",
            personalSupport="OFF",
            executionTime=0
        )
    )
    favourite_strategy = models.JSONField(default = list) # List of all favourite strategies
    broker_information = models.JSONField(
        default=dict(defaultBroker={}, otherBroker={})
    )
    def __str__(self):
        return self.username

class Strategy(models.Model):
    # Core Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    is_active = models.CharField(max_length=20, choices=[  # status of Algo 
        ('active', 'Active'), # Live 
        ('inactive', 'Inactive'), # Temporary off
        ('disabled', 'Disabled') # Permanently disabled / under maintainance
    ], default='Disabled')
    mode = models.CharField(
        max_length=20,
        choices=[
            ('intraday', 'Intraday'),
            ('swing', 'Swing')
        ],
        default='Intraday'
    )  # Trading style
    segment = models.CharField(
        max_length=50,
        choices=[
            ('NSE_EQ', 'NSE Equity'),
            ('NSE_FNO', 'NSE FnO'),
            ('Forex', 'Forex'),
            ('US_Equity', 'US Equity'),
            ('Commodity', 'Commodity'),
        ],
        default='NSE_FNO'
    )  # Market or asset class
    instruments = JSONField(default=list) # ["Reliance", "Zomato"] etc

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.CharField(max_length=10, default="1.0.0") # Performance tracking for multiple Version
    tags = JSONField(default=list)  # ["Price Exit", "Stop-Loss"]
    # Text  Content
    short_description = models.TextField(null=True, blank=True)
    strategy_breakdown = models.JSONField(null=True, blank=True,
        default = dict(
            stratefyBreakdown = "",
            entryCondition = "",
            exitCondition = "",
            keyPoints = ""
        )
    )

    subscription_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    min_required_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    user_count = models.PositiveIntegerField(default=0)  # Subscribed by user

    parameters = models.JSONField(default = dict(
            maxRisk = None,
            takeProfit = None,
            successRate = None,
            # Depends on strategy
        )
    )
    total_trades = models.PositiveIntegerField(default=0)  # Number of trades executed till now

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
    # Record of Real accounts subscribed to a specific strategy
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Links to CustomUser
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)  # Links to Strategy
    additional_info = models.JSONField(blank=True, null=True)  # Any additional subscription-related data
    type = models.CharField(max_length=10,
        choices=[  # Type of Strategy
            ('demo', 'Demo'),
            ('real', 'Real')
        ],
        default = "demo"
    )
    def __str__(self):
        return f"{self.user.username} subscribed to {self.strategy.name}"


class TradeLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tradelogs")  # Link to the user
    Strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)  # Link to the algorithm
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
    strategy = models.ForeignKey(Strategy, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")  # Nullable for non-algo-specific transactions
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)  # Amount charged for the transaction
    transaction_status = models.CharField(max_length=15, choices=TRANSACTION_STATUS, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)  # When the user requested the transaction
    completion_date = models.DateTimeField(null=True, blank=True)  # When the transaction was completed
    description = models.TextField(null=True, blank=True)  # Optional: Additional details

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount} - {self.transaction_status}"
