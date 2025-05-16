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
    path('strategies',views.strategies_list, name ='strategies_list'),
    path('strategies/<str:strategy_id>',views.strategies_details, name ='strategies_details'),
    path('pricing',views.pricing, name ='pricing'),
    path('admin/', admin.site.urls),
    ]