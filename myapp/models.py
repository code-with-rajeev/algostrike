from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import uuid

# Define default dictionaries as callable functions
def get_default_active_plan_details():
    return {
        "activePlan": {},  # {"planID": planID, "name": planName}
        "expiredPlan":{}  # Recently expired plan
    }

def get_default_preference():
    return { "theme":"Light", "notification":"Yes"}

def get_default_profile_information():
    return {
        "tradingExperience":"",
        "interestedProduct":"",
        "codingExperience":"",
        "tradingGoal":""
    }

def get_default_strategy_information():
    return {
        "strategiesSaved":0, # created / customized by user 
        "runningStrategies":0,
        "analyticAccess":"OFF",
        "personalSupport":"OFF",
        "executionTime":0
    }

def get_default_favourite_strategy():
    return []

def get_default_broker_information():
    return { "defaultBroker":{}, "otherBroker":{}}

def get_default_instruments():
    return {}

def get_default_tags():
    return []

def get_default_strategy_breakdown():
    return {
        "strategyBreakdown" : "",
        "executionLogic" : {},
        "keyPoints" : []
    }

def get_default_parameters():
    return {
        "maxRisk": None,
        "takeProfit": None,
        "successRate": None,
    }

def get_default_additional_info():
    return {}

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    fund_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0) # Wallet balance
    date_joined = models.DateTimeField(default=now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    active_plan_details = models.JSONField(default=get_default_active_plan_details)
    preference = models.JSONField(default=get_default_preference)
    profile_information = models.JSONField(default=get_default_profile_information)
    strategy_information = models.JSONField(default=get_default_strategy_information)
    favourite_strategy = models.JSONField(default=get_default_favourite_strategy)
    broker_information = models.JSONField(default=get_default_broker_information)

    def __str__(self):
        return self.username

    class Meta:
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
        ]

class Strategy(models.Model):
    # Core Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    is_active = models.CharField(max_length=20, choices=[
        ('active', 'Active'), # Live 
        ('inactive', 'Inactive'), # Temporary off
        ('disabled', 'Disabled') # Permanently disabled / under maintainance
    ], default='disabled')

    algo_type = models.CharField(max_length=20, choices=[
        ('custom_technical', 'Custom '), # Pure technical based Algo Model
        ('ai_model', 'Advance Trained Model') # AI based Algo Model
    ], default='model')

    mode = models.CharField(
        max_length=20,
        choices=[
            ('intraday', 'Intraday'),
            ('swing', 'Swing')
        ],
        default='intraday'
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
    instruments = models.JSONField(default=get_default_instruments) # ["Reliance", "Zomato"] etc

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.CharField(max_length=10, default="1.0.0") # Performance tracking for multiple Version
    tags = models.JSONField(default=get_default_tags)  # ["Price Exit", "Stop-Loss"]
    # Text  Content
    short_description = models.TextField(null=True, blank=True)
    strategy_breakdown = models.JSONField(blank=True, default=get_default_strategy_breakdown)

    subscription_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    min_required_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    user_count = models.PositiveIntegerField(default=0)  # Subscribed by user

    parameters = models.JSONField(default=get_default_parameters)
    total_trades = models.PositiveIntegerField(default=0)  # Number of trades executed till now

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Strategy"

# Separate Demo-Trade Log for performance of the Algorithm
class StrategyTradeLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)  # Foreign key to identify which algo this log is for
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)  # Timestamp of trade execution
    trade_type = models.CharField(max_length=10, choices=[
        ('buy', 'Buy'),
        ('sell', 'Sell')
    ])
    quantity = models.IntegerField(default=0)  # Number of units traded
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at which trade occurred
    profit_loss = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Profit or loss from trade
    additional_info = models.JSONField(default=get_default_additional_info, blank=True)  # Optional field for additional data
    def __str__(self):
        return f"Algo {self.strategy.name} Trade Log {self.id} at {self.timestamp}"
        
    class Meta:
        indexes = [
            models.Index(fields=['timestamp'], name='timestamp_idx'),
        ]
        verbose_name_plural = "Strategy TradeLog"

class Subscription(models.Model):
    # Record of Real accounts subscribed to a specific strategy
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Links to CustomUser
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)  # Links to Strategy
    additional_info = models.JSONField(blank=True, default=get_default_additional_info)  # Any additional subscription-related data
    quantity = models.IntegerField(default=0)  # Number of units 
    profit_loss = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Profit or loss from trade

    algo_type = models.CharField(max_length=10,
        choices=[
            ('demo', 'Demo'),
            ('real', 'Real')
        ],
        default="demo"
    )
    algo_status = models.CharField(max_length=10, choices=[
        ('open', 'Open'),
        ('close', 'Close')
    ], default='close')
    def __str__(self):
        return f"{self.user.username} subscribed to {self.strategy.name}"

class Plans(models.Model):
    plan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan_type = models.CharField(max_length=100, unique=True)  # Plan name
    plan_price = models.PositiveIntegerField()  # Integer price
    price_symbol = models.CharField(max_length=3, default='INR')  # Currency symbol, e.g., INR
    max_capital_allowed = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)  # Maximum capital allowed
    live_trading = models.BooleanField(default=False)  # Live trading yes/no
    concurrent_executions_live = models.PositiveIntegerField(default=0)  # Number of concurrent executions (live trading)
    concurrent_executions_all = models.PositiveIntegerField(default=0)  # Number of concurrent executions (all)
    execution_time_bt_pt = models.PositiveIntegerField(default=0)  # Execution time for backtesting & paper trading (in minutes)
    personal_support = models.BooleanField(default=False)  # Personal support yes/no
    pnl_tracker = models.BooleanField(default=False)  # P&L tracker yes/no

    def __str__(self):
        return self.plan_type

    class Meta:
        verbose_name_plural = "Available Plans"

class UserPlanSubscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='plan_subscriptions')
    plan = models.ForeignKey(Plans, on_delete=models.PROTECT, related_name='user_subscriptions')
    
    # Replicated plan configuration fields to freeze at subscription time
    plan_type = models.CharField(max_length=100)  # Copied from Plans.plan_type
    plan_price = models.PositiveIntegerField()  # Copied from Plans.plan_price
    price_symbol = models.CharField(max_length=3)  # Copied from Plans.price_symbol
    max_capital_allowed = models.DecimalField(max_digits=15, decimal_places=2)  # Copied from Plans.max_capital_allowed
    live_trading = models.BooleanField()  # Copied from Plans.live_trading
    concurrent_executions_live = models.PositiveIntegerField()  # Copied from Plans.concurrent_executions_live
    concurrent_executions_all = models.PositiveIntegerField()  # Copied from Plans.concurrent_executions_all
    execution_time_bt_pt = models.PositiveIntegerField()  # Copied from Plans.execution_time_bt_pt
    personal_support = models.BooleanField()  # Copied from Plans.personal_support
    pnl_tracker = models.BooleanField()  # Copied from Plans.pnl_tracker
    
    # Subscription-specific fields
    subscription_timestamp = models.DateTimeField(auto_now_add=True)  # When the subscription was created
    validity_hours_left = models.FloatField(default=0.0)  # Remaining validity in hours
    is_active = models.BooleanField(default=True)  # Whether the subscription is currently active

    def __str__(self):
        return f"{self.user.username} - {self.plan_type} (Subscribed: {self.subscription_timestamp})"

    class Meta:
        indexes = [
            models.Index(fields=['user', 'subscription_timestamp'], name='user_subscription_idx'),
            models.Index(fields=['plan', 'is_active'], name='plan_active_idx'),
        ]
        verbose_name_plural = "User Plan Subscriptions"

class TradeLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tradelogs")  # Link to the user
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)  # Link to the algorithm
    timestamp = models.DateTimeField(auto_now_add=True)  # When the trade was executed
    trade_type = models.CharField(max_length=10, choices=[
        ('buy', 'Buy'),
        ('sell', 'Sell')
    ])
    trade_status = models.CharField(max_length=10, choices=[
        ('open', 'Open'),
        ('close', 'Close')
    ], default='open')
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)  # Entry price of the trade
    exit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Exit price, if applicable
    quantity = models.IntegerField()  # Number of units traded
    pnl = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Profit or Loss from the trade
    strategy_notes = models.TextField(blank=True, null=True)  # Optional notes about the trade (e.g., strategy used)
    additional_info = models.JSONField(blank=True, default=get_default_additional_info) # Additional trade-related information

    def __str__(self):
        return f"Trade by {self.user.username} on {self.strategy.name} at {self.timestamp}"

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

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
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