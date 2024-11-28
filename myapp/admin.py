from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Subscription, Algo, AlgoTradeLog, TradeLog, Transaction
#register model to show it in admin panel OPTIONAL
admin.site.register(CustomUser)
admin.site.register(Subscription)
admin.site.register(Algo)
admin.site.register(AlgoTradeLog)
admin.site.register(TradeLog)
admin.site.register(Transaction)