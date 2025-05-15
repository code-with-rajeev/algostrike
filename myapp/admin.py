from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Subscription, Strategy, StrategyTradeLog, TradeLog, Transaction, Plans, UserPlanSubscription
#register model to show it in admin panel OPTIONAL
admin.site.register(CustomUser)
admin.site.register(Subscription)
admin.site.register(Strategy)
admin.site.register(StrategyTradeLog)
admin.site.register(TradeLog)
admin.site.register(Transaction)
admin.site.register(Plans)
admin.site.register(UserPlanSubscription)