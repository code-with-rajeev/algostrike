from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
   
 # Note: Make sure to redirect these URL from frontend to backend. Temporary Backend and Frontend are running on same server Vercel.
    path('api/broker/authenticate/broker_credentials',views.broker_credentials, name ='broker_credentials'),
    path('api/broker/authenticate/verify_broker',views.verify_broker, name ='verify_broker'),
    path('api/test/test_server',views.test_server, name ='test_server'),
    path('api/test/debug_mode',views.debug_mode, name ='debug_mode'),
    path('api/user/authenticate/generate_otp',views.generate_otp, name ='generate_otp'),
    path('api/user/authenticate/verify_otp',views.verify_otp, name ='verify_otp'),

    # Strategies
    path('api/strategies',views.strategies_list, name ='strategies_list'),
    path('api/strategies/<str:strategy_id>',views.strategies_details, name ='strategies_details'),

    # Dashboard
    path('api/dashboard/profileInfo',views.profile_info,name='profile_info'),
    path('api/dashboard/accountInfo',views.account_info,name='account_info'),
    path('api/dashboard/subscriptionInfo',views.subscription_info,name='subscription_info'),

    # Plans
    path('api/pricing',views.available_plans, name ='available_plans'),
    path('api/pricing/<str:plan_id>/purchase',views.purchase_plan, name ='purchase_plan')

    path('admin/', admin.site.urls),
    ]