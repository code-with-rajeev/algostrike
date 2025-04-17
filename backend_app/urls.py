from django.urls import path
from . import views

urlpatterns = [
   
 # Note: Make sure to redirect these URL from frontend to backend. Temporary Backend and Frontend are running on same server Vercel.
    path('broker_credentials',views.broker_credentials, name ='broker_credentials'),
    path('verify_broker',views.verify_broker, name ='verify_broker'),
    path('',views.test_server, name ='test_server'),
    path('admin/', admin.site.urls),
    ]
