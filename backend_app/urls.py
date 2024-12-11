from django.urls import path
from . import views

urlpatterns = [
 # Url for Gunicorn test purpose
    path('test/',views.test_view, name ='test_view'),
    ]