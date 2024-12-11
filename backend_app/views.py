from django.http import HttpResponse as HR

# Create your views here.
def test_view(request):
    return HR("Gunicorn Running!")