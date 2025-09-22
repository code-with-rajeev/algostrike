from django.urls import path
from . import views

urlpatterns = [
 #' ' empty means main site/project
    #path('',views.index, name ='index'),
    #path('home',views.home, name ='home'),
    path('features',views.feature, name ='features'),
    path('guide',views.guide, name ='guide'),
    path('contact',views.contact_us, name ='contact_us'),
    # log in mechanism
    path('login',views.login_view, name ='login'),
    path('logout',views.logout_view, name ='logout'),
    path('register',views.register, name ='register'),
    # dashboard view
    path('dashboard',views.dashboard, name ='dashboard'),
    path('strategies',views.strategies, name ='strategies'),
    path('subscription',views.subscription, name ='subscription'),
    path('reports',views.reports, name ='reports'),
    path('wizard',views.wizard, name ='wizard'),
    # others
    path('add_broker',views.add_broker, name ='add_broker'),
    path('portfolio',views.portfolio_view, name ='portfolio'),
    path('create_trade',views.create_trade, name ='create_trade'),
    path('user_trades',views.user_trades, name ='user_trades'),

    # side project
    path('', views.index, name = 'index'),
    path('home', views.home, name = 'home'),
    path('api/doctor_admin', views.doctor_admin, name = "Doctor's Admin Page"),
    path('api/manage_patient', views.manage_patient, name = 'Manage Patient'),
    path('api/manage_patient/updates', views.fetch_patient_updates, name = 'fetch patient updates'),
    path('api/assistant', views.assistant_page, name = "Assistant's Page"),
    path('api/audio_snippet/parse', views.audio_parse, name = "Parse Audio to AiAgent"),
    ]
