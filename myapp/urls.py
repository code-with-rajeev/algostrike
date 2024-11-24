from django.urls import path
from . import views

urlpatterns = [
 #' ' empty means main site/project
    path('',views.index, name ='index'),
    path('home',views.home, name ='home'),
    path('features',views.feature, name ='features'),
    path('guide',views.guide, name ='guide'),
    path('contact',views.contact_us, name ='contact_us'),
    # log in mechanism
    path('login',views.login_view, name ='login'),
    path('logout',views.logout_view, name ='logout'),
    path('register',views.register, name ='register'),
    path('portfolio',views.portfolio_view, name ='portfolio'),
    path('create_trade',views.create_trade, name ='create_trade'),
    path('user_trades',views.user_trades, name ='user_trades'),
    ]
