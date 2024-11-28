from django.shortcuts import render, redirect
from django.http import HttpResponse as HR #add this
from django.contrib.auth.decorators import login_required #protect portfolio access
from django.contrib.auth import authenticate, login, logout #for login, logout
from django.contrib import messages 
from django.shortcuts import render, redirect
from .models import TradeLog
from django.contrib.auth.hashers import make_password
from myapp.models import CustomUser

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


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('portfolio')  # Redirect to portfolio page after login
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


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

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # Check for existing data
        if CustomUser.objects.filter(email__iexact=email).exists():
            return render(request, 'register.html',{'message':'Email already exists'})
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html',{'message':'Username already exists'})



        # Create and save the new user with default PnL and Invested
        try:
            new_user = CustomUser.objects.create(
            username=username,
            email=email,
            password=make_password(password),  # Hash the password
            )
            new_user.save()            
        except IntegrityError:
            return render(request, 'register.html',{'message':'Something Went Wrong'})
        # Redirect to the login page
        return redirect('portfolio')

    return render(request, 'register.html',{'message':'Please enter unique credentials only'})


