from django.shortcuts import render
from django.http import HttpResponse as HR #add this

# Create your views here.
def index(request):
    return render(request, 'index.html')
def home(request):
    return render(request, 'index.html')
def contact_us(request):
    return render(request, 'contact us.html')
def feature(request):
    return render(request, 'features.html')

def guide(request):
    return render(request, 'guide.html')
