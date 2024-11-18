from django.urls import path
from . import views

urlpatterns = [
 #' ' empty means main site/project
    path('',views.index, name ='index'),
    path('home',views.home, name ='home'),
    path('features',views.feature, name ='features'),
    path('guide',views.guide, name ='guide'),
    path('contact',views.contact_us, name ='contact_us'),
    ]
