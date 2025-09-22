from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from myapp.models import CustomUser
from myapp.models import Strategy
from myapp.models import Plans
from myapp.models import UserPlanSubscription
from myapp.utils import is_valid_username
import json
# Module required for authentication
from backend.core.authentication.authenticate_broker.authenticate import authenticate
from django.views.decorators.csrf import csrf_exempt
from backend_app.backend.core.authentication.authenticate_user import verification as user_verification

# Custom decorator to allow any origin for CORS
# Only For Testing

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


def allow_any_origin(view_func):
    def wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'  # Allow all origins
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTION'
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'
        response['Access-Control-Allow-Credentials'] = 'true'  # Allow cookies for session/CSRF
        return response
    return wrapped_view

# For testing API
def api_testing(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            secret_testing_key = data.get("secret_testing_key")
            if secret_testing_key == os.environ.get("TESTING_KEY"):
                return True
        return False
    except Exception as a:
        return False

# This function generates OTP
@csrf_exempt
def generate_otp(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')

            #if not all([otp, username]):
            if not all([email, username,password]):
                return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)
            # Validate input
            if not is_valid_username(username):
                return JsonResponse({'success': False, 'message': 'Username must be at least 7 characters and contain only a-z, A-Z, 0-9, or _'})            
            # Check whether email/username already in use
            if CustomUser.objects.filter(email__iexact=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already exists'})
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists'})
            # Generates 6-digit random OTP
            response = user_verification.generate_otp(username, email)
            return JsonResponse(response) 
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            otp = data.get('otp')

            #if not all([otp, username]):
            if not all([email, username,password]):
                return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)
            # Validate input
            if not is_valid_username(username):
                return JsonResponse({'success': False, 'message': 'Username must be at least 7 characters and contain only a-z, A-Z, 0-9, or _', "type":"invalid regex"})            
            # Check whether email/username already in use
            # if (exists): return JsonResponse({'success': False, 'message': 'Username/Email already exist'})
            if CustomUser.objects.filter(email__iexact=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already exists'})
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists'})
            
            response = user_verification.verify_otp(email,otp)
            return JsonResponse(response) 
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

"""
Dashboard : Working
"""
#@login_required
# CSRF Needed
# Allow Only Post method

#@allow_any_origin
def profile_info(request):
    # For API Testing only!
    if not api_testing(request):
        JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource. Please provide valid secret_testing_key.'}, status = 403)
    #if request.method == 'POST':
    if True: # For testing
        try:
            if not request.user.is_authenticated:
            # Redirect Login
                return JsonResponse({"success": False, "message": "Anonymous user"}, status=401)
            #qwery = request.GET.get("query")
            data = CustomUser.objects.filter(username=request.user).values(
                "username","email","phone","fund_balance","date_joined","preference","profile_information").first()
            response = {
                "success": True,
                "data": data
            }
            return JsonResponse(response)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

#@allow_any_origin
def account_info(request):
    # For API Testing only!
    if not api_testing(request):
        JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource. Please provide valid secret_testing_key.'}, status = 403)

    #if request.method == 'POST':
    if True: # For testing
        try:
            if not request.user.is_authenticated:
            # Redirect Login
                return JsonResponse({"success": False, "message": "Anonymous user"}, status=401)
            #qwery = request.GET.get("query")
            data = CustomUser.objects.filter(username=request.user).values(
                "is_active","date_joined","last_login","fund_balance","broker_information").first()
            response = {
                "success": True,
                "data": data
            }
    
            return JsonResponse(data)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

#@allow_any_origin
def subscription_info(request):
    # For API Testing only!
    if not api_testing(request):
        JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource. Please provide valid secret_testing_key.'}, status = 403)

    #if request.method == 'POST':
    if True: # For testing
        try:
            if not request.user.is_authenticated:
            # Redirect Login
                return JsonResponse({"success": False, "message": "Anonymous user"}, status=401)
            #query = request.GET.get("query")
            
            data = CustomUser.objects.filter(username=request.user).values(
                "active_plan_details","favourite_strategy","strategy_information").first()
            response = {
                "success": True,
                "data": data
            }
            return JsonResponse(data)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


"""
Strategies : Working
"""
#@allow_any_origin
def strategies_details(request, strategy_id):
    # For API Testing only!
    if not api_testing(request):
        JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource. Please provide valid secret_testing_key.'}, status = 403)

    # Need Testing / No Auth req
    # You can also return from cache
    # if request.method == "POST":
    if True: # For testing
        try:
            if not Strategy.objects.filter(id = strategy_id).exists():
                return JsonResponse({'success': False, 'message': 'Invalid Strategy'}, status=405)
            query = request.GET.get("query")
            if query in ["addFavourites","addPortfolio","requestCustomization"]:
                if not request.user.is_authenticated:
                    return JsonResponse({"success": False, "message": "Anonymous user can't access this"}, status=401)
                # User must login to update
                if query == "addFavourites":
                    method = request.GET.get("method","true")
                    # Get the user instance
                    instance = CustomUser.objects.get(username = request.user)
                    if method == "true":
                        if strategy_id not in instance.favourite_strategy:
                            instance.favourite_strategy.append(strategy_id)
                            instance.save()
                        return JsonResponse({"success": True, "message": "Sucessfully Added to Favourites"}, status=200)
                    # This step must be done via DELETE method
                    elif method == "false":
                        if strategy_id in instance.favourite_strategy:
                            instance.favourite_strategy.remove(strategy_id)
                            instance.save()
                        return JsonResponse({"success": True, "message": "Sucessfully Removed from Favourites"}, status=200)
                elif query == "addPortfolio":
                    method = request.GET.get("method","true")
                    if method == "true":            
                        return JsonResponse({"success": True, "message": "Sucessfully Added to Portfolio"}, status=200)
                    # This step must be done via DELETE method
                    elif method == "false":
                        return JsonResponse({"success": True, "message": "Sucessfully Removed from Portfolio"}, status=200)
                elif query == "requestCustomization":
                    return JsonResponse({'success': False, 'message': 'This feature is not Available'}, status=405)

                return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
            # No expected query
            data = Strategy.objects.filter(id = strategy_id).values() # fetch all values
            response = []
            for strategy in data:
                strategy['id'] = strategy_id
                response.append(strategy)
            return JsonResponse({'success': True, 'message': f'Fetched Available Strategies', 'data': response}, status = 200)
        except Exception as a:
           return JsonResponse({'success': True, 'message': f'Error fetching Strategies: {a}', 'data': []}, status = 500)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

#@allow_any_origin
def strategies_list(request):
    # For API Testing only!
    if not api_testing(request):
        JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource. Please provide valid secret_testing_key.'}, status = 403)

    # Need Testing / No Auth req
    # You can also return from cache
    # Missing Pagination / Partial data fetching
    args = [
        'id','name','mode','segment','instruments',
        'version','tags','short_description','min_required_funds',
        'user_count'
        ]
    # if request.method == "POST":
    if True: # For testing
        try:
            query = request.GET.get("sortBy")
            data = []
            if query:
                # Expect a valid query
                if query == "minCapitalReq":
                    # Sort via min req funds
                    order = request.GET.get("order","asc")
                    ordering = 'min_required_funds' if order == 'asc' else '-min_required_funds'
                    data = Strategy.objects.all().order_by(ordering).values(*args) # fetch all values
                    
                elif query == "favourite":
                    if request.user.is_authenticated:
                        fav_list = CustomUser.objects.get(username=request.user).favourite_strategy
                        if fav_list:
                            data = Strategy.objects.filter(id__in=fav_list).values(*args) # fetch all fav_strategies
                else:
                    # Invalid query, fetch default
                    data = Strategy.objects.all().values(*args) # fetch all values
            else:
                # No expected query
                data = Strategy.objects.all().values(*args) # fetch all values
            response = []
            for strategy in data:
                strategy['id'] = str(strategy['id'])
                response.append(strategy)
            return JsonResponse({'success': True, 'message': f'Fetched Available Strategies', 'data': response}, status = 200)
        except Exception as a:
            return JsonResponse({'success': False, 'message': f'Error fetching Strategies', 'data': []}, status = 500)


"""
Plans : Payment GateWay not Integrated
"""
#@allow_any_origin
def available_plans(request):
    # For API Testing only!
    if not api_testing(request):
        JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource. Please provide valid secret_testing_key.'}, status = 403)

    # Need Testing / No Auth req
    # You can also return from cache
    #if request.method == 'POST':
    if True: # For testing
        try:
            #query = request.GET.get("query")            
            data = Plans.objects.all().values()# fetch available plans
            response = []
            for plan in data:
                plan['plan_id'] = str(plan['plan_id'])
                response.append(plan)
            return JsonResponse({'success': True, 'message': f'Fetched Available Plans', 'data': response}, status = 200)
    
        except Exception as a:
            return JsonResponse({'success': True, 'message': f'Error fetching Plans', 'data': []}, status = 500)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

#@allow_any_origin
def purchase_plan(request, plan_id):
    # For API Testing only!
    if not api_testing(request):
        JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource. Please provide valid secret_testing_key.'}, status = 403)

    # Need Testing / Auth req
    # You can also return from cache
    # if request.method == 'POST':
    if True: # For testing
        try:
            # Validate Authentication
            if not request.user.is_authenticated:
                    return JsonResponse({"success": False, "message": "Anonymous user can't access this feature"}, status=401)
            # Check if such plan exists            
            if not Plans.objects.filter(plan_id = plan_id).exists():
                return JsonResponse({'success': False, 'message': 'Invalid Plan Request'}, status=405)
            query = request.GET.get("method")
            if query == 'testing':
                # Fetch requested plan details
                selected_plan = Plans.objects.get(plan_id = plan_id)
                current_user = data = CustomUser.objects.get(username=request.user)
                # Either create new or extend expiry
                subscription, created = UserPlanSubscription.objects.get_or_create(
                    user = current_user,
                    plan = selected_plan,
                    plan_type = selected_plan.plan_type,
                    plan_price = selected_plan.plan_price,
                    max_capital_allowed = selected_plan.max_capital_allowed,
                    live_trading = selected_plan.live_trading,
                    concurrent_executions_live = selected_plan.concurrent_executions_live,
                    concurrent_executions_all = selected_plan.concurrent_executions_all,
                    execution_time_bt_pt = selected_plan.execution_time_bt_pt,
                    personal_support = selected_plan.personal_support,
                    pnl_tracker = selected_plan.pnl_tracker,
                    validity_hours_left = 720 # 30 Days
                    )
                if not created:
                    subscription.validity_hours_left += 720
                    subscription.save()
                    current_user.active_plan_details['activePlan'] = {"subscriptionID": str(subscription.id), "planType": subscription.plan_type}
                    current_user.strategy_information["personalSupport"]=selected_plan.personal_support
                    current_user.strategy_information["executionTime"]=selected_plan.execution_time_bt_pt
                    
                    current_user.save()
                    return JsonResponse({'success': True, 'message': 'Plan Already Exists, Validity increased by 30 Days'}, status=200)
                else:
                    current_user.active_plan_details['activePlan'] = {"subscriptionID": str(subscription.id), "planType": subscription.plan_type}
                    current_user.strategy_information["personalSupport"]=selected_plan.personal_support
                    current_user.strategy_information["executionTime"]=selected_plan.execution_time_bt_pt
                    current_user.save()
                    return JsonResponse({'success': True, 'message': 'Congratulation! New Plan Added'}, status=200)
                    
        except Exception as a:
            return JsonResponse({'success': False, 'message': f'Purchase failed: {a}'}, status=405)           
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)



"""
Others : Avoid these API / Under Testing
"""
@csrf_exempt  # Disable CSRF for simplicity (only in development)
def broker_credentials(request):
    # For API Testing only!
    if not api_testing(request):
        JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource. Please provide valid secret_testing_key.'}, status = 403)

    return JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource'}, status = 403)
    # Forbidden
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            # Note: Temporary kotak Neo authentication will work only, seperate authentication is required for seperate broker

            data = json.loads(request.body)
            broker = data.get('broker')
            credentials = data 
            # root/backend/core/authentication/authenticate_broker/authenticate_broker.py
            # authenticate_broker.authenticate(credentials) 
            # return - > JSON reponse {success: [True/False], data: [token, error_type], error: error, status: []}
            response = authenticate(credentials)
            # Note: if response.success == True, means OTP has been sent to the CLIENT registered number.

            if response['success']:
                # temporary storing credentials securely before otp verification(e.g., database, secure storage)
                # Optional: [ IMP ] Prefer redis to store credentials temporarily with 5min timeout temporarily.
                # store_credentials(customer_key, customer_secret, password, mobile_number).
                return JsonResponse({'success': True, 'message': 'OTP sent to mobile number'})
            else:
                return JsonResponse({'success': False, 'message': response['message']}, status=response['status'])
            
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def verify_broker(request):
    # For API Testing only!
    if not api_testing(request):
        JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource. Please provide valid secret_testing_key.'}, status = 403)

    #global mobile_number
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            otp = data.get('otp')

            # Validate input
            #if not all([otp, mobile_number]):
            if not otp:
                return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)

            # Simulate OTP verification with the broker (replace with actual API call)
            if otp == '12345':
                otp_valid = True
            else:
                otp_valid = False # Replace with broker's API response

            if otp_valid:
                # Retrieve stored credentials from cache/database/temporary_variable

                """
                Redis example
                cache_key = f"broker_temp_{mobile_number}"
                credentials = cache.get(cache_key)
                """
                
                #if credentials:
                if True:
                    # Store credentials permanently (e.g., in a database)
                    # print(f"Storing credentials for {mobile_number} credentials")

                    # Clear temporary cache
                    # cache.delete(cache_key)

                    return JsonResponse({'success': True, 'message': 'Broker added successfully (This is mock response for testing. OTP validation is bypassed)'}, status = 200)
                else:
                    return JsonResponse({'success': False, 'message': 'Temporary credentials not found (This is mock response for testing. Enter OTP=12345, validation will be bypassed)'}, status=404)
            else:
                return JsonResponse({'success': False, 'message': 'Invalid OTP'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

def test_server(request):    
    return JsonResponse({'success': True, 'message': f'Backend is running without errors!'})

def store_credentials(customer_key, customer_secret, password, mobile_number):
    # For API Testing only!
    if not api_testing(request):
        JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource. Please provide valid secret_testing_key.'}, status = 403)
    # Simulate storing credentials (replace with actual database or secure storage logic)
    print(f"Storing credentials: {customer_key}, {customer_secret}, {password}, {mobile_number}")
    # Example: Save to database or encrypted storage
    pass
    
def debug_mode(request):
    # For API Testing only!
    if not api_testing(request):
        JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource. Please provide valid secret_testing_key.'}, status = 403)
    """
    try:
        from .tasks import schedule_algo, schedule_stream_worker
        schedule_algo.delay()
        schedule_stream_worker()
        return JsonResponse({'success': True}, status=200)
    except Exception as a:
        return JsonResponse({'success': False, 'message': f'Error : {a}'}, status=400)
    """
    pass