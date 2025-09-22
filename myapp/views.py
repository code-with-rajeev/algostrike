from django.shortcuts import render, redirect
from django.http import HttpResponse as HR #add this
from django.contrib.auth.decorators import login_required #protect portfolio access
from django.contrib.auth import authenticate, login, logout #for login, logout
from django.contrib import messages 
from django.shortcuts import render, redirect
from .models import TradeLog
from django.contrib.auth.hashers import make_password
from myapp.models import CustomUser
from myapp.utils import is_valid_username
from myapp import parser
# from backend.interfaces.cache_manager import CacheManager


# Side Project

# POST API
def fetch_patient_updates(request):
    # Redis-> "{doctor_ID}:manage_patient" : {"ongoingPatient": [max = 1?], "pendingAppointment": [], "appointedPatients": [] }
    return JsonResponse({"status":True, "message": "API under maintainance"})
# Create your views here.
def index(request):
    return render(request, 'manage_patient.html')

def home(request):
    return render(request, 'manage_patient.html')

def doctor_admin(request):
    return render(request, "doctor_admin.html")


def manage_patient(request):
    # fetch all pending appointments and last 10 appointed from DB/cache

    # dummy data
    
    suggestionData = {
        "case": ["Fever", "Cough", "Diabetes", "Back Pain"],
        "cause": ["Infection", "Stress", "Allergy", "Injury"],
        "medicine": ["Paracetamol", "Ibuprofen", "Amoxicillin", "Cetirizine"]
    }
    
    data = {"suggestionData": suggestionData, "timing": ""}
    return render(request, "manage_patient.html", {"data":data})

def assistant_page(request):
    # fetch all pending appointments and last 10 appointed from DB/cache

    # dummy data
    pendingAppointments = [
      {"id":"APT101", "name":"Ravi Kumar", "number":"9876543210", "date":"2025-09-17", "followup":"2025-09-22", "status":"pending"},
      {"id":"APT102", "name":"Sita Sharma", "number":"9123456780", "date":"2025-09-18", "followup":"2025-09-23", "status":"pending"},
      {"id":"APT103", "name":"Aman Gupta", "number":"9988776655", "date":"2025-09-19", "followup":"2025-09-25", "status":"pending"}
    ]
    appointedPatients = [
      {"id":"APT090", "name":"Arjun Mehta", "number":"9090909090", "date":"2025-09-10", "followup":"2025-09-18", "status":"appointed"},
      {"id":"APT091", "name":"Priya Singh", "number":"8080808080", "date":"2025-09-12", "followup":"2025-09-20", "status":"appointed"}
    ]
    data = {"pendingAppointments": pendingAppointments, "appointedPatients": appointedPatients}
    return render(request, "assistant.html", {"data":data})

@csrf_exempt
def audio_parse(request):
    try:
        if request.method == 'POST':
            data = request.body.decode("utf-8")
            suggestion = parser.parse_input(data)
            if suggestion["status"] != False:
                return JsonResponse(suggestion)
            return JsonResponse({"status":False, "message": suggestion["message"]})
    except Exception as a:
        print(a)
        return JsonResponse({"status":False, "message": "INVALID REQUEST"})

# Create your views here.
"""
def index(request):
    return render(request, 'index.html')
def home(request):
    return render(request, 'index.html')
"""
def contact_us(request):
    return render(request, 'contact us.html')
def feature(request):
    return render(request, 'features.html')

def guide(request):
    return render(request, 'guide.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not is_valid_username(username):
            messages.error(request, "Username must be at least 7 characters and contain only a-z, A-Z, 0-9, or _")
            return render(request, 'login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to portfolio page after login
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    # Signup is handled via OTP-based authentication from backend_app.views.generate_otp
    if request.method == 'GET':
        return render(request, 'register.html',{'message':'Please enter unique credentials only'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

#Dashboard View
@login_required
def dashboard(request):
    #trades = TradeLog.objects.all()
    #return render(request, 'portfolio.html', {'trades': trades})
    return render(request, 'dashboard.html', {'name': request.user.username})

#Allow Access
def strategies(request):
    
    return render(request, 'strategies.html',{'message':'No Strategies yet !', 'name': request.user.username})
    
@login_required
def subscription(request):
    
    return render(request, 'subscription.html', {"message":"You Don't have any Subscription yet !", 'name': request.user.username})

@login_required
def reports(request):
    
    return render(request, 'reports.html', {'message':'No Reports to show !','name': request.user.username})
    
@login_required
def wizard(request):
    
    return render(request, 'wizard.html', {'message':'This Strategy Builder feature will be available soon !', 'name': request.user.username})
    

# Other Backend services
@login_required
def add_broker(request):
    # check whether broker's credentials already exists. If Yes, fetch them and return.
    return render(request, 'add_broker.html',{'available_brokers':'No available brokers []'})

@login_required
def portfolio_view(request):
    #trades = TradeLog.objects.all()
    #return render(request, 'portfolio.html', {'trades': trades})
    if not request.user.is_authenticated:
        return redirect(f'/login/?next={request.path}')
    return render(request, 'portfolio.html')

@login_required
def create_trade(request):
    """
    if request.method == 'POST':
        trade_type = request.POST['trade_type']
        symbol = request.POST['symbol']
        quantity = request.POST['quantity']
        price = request.POST['price']
        
        # Create a new Trade record
        trade = TradeLog(
            user=request.user,
            trade_type=trade_type,
            symbol=symbol,
            quantity=quantity,
            price=price
        )
        trade.save()
        return redirect('user_trades')  # Redirect to a page showing all trades
    """
    return render(request, 'create_trade.html')

@login_required
def user_trades(request):
    """
    trades = TradeLog.objects.filter(user=request.user)  # Fetch all trade records
    return render(request, 'user_trades.html', {'trades': trades})
    """
    return render(request, 'user_trades.html') #remove it later