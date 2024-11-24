from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Trade, TradeLog
#register model to show it in admin panel OPTIONAL
admin.site.register(CustomUser)
admin.site.register(Trade)
admin.site.register(TradeLog)