from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from myapp.models import CustomUser
from myapp.utils import is_valid_username
import json
# Module required for authentication
from backend.core.authentication.authenticate_broker.authenticate import authenticate
from django.views.decorators.csrf import csrf_exempt
from backend_app.backend.core.authentication.authenticate_user import verification as user_verification

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
                return JsonResponse({'success': False, 'message': 'Username must be at least 7 characters and contain only a-z, A-Z, 0-9, or _'})            
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


@csrf_exempt  # Disable CSRF for simplicity (only in development)
def broker_credentials(request):
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
    return JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource'}, status = 403)
    # Simulate storing credentials (replace with actual database or secure storage logic)
    print(f"Storing credentials: {customer_key}, {customer_secret}, {password}, {mobile_number}")
    # Example: Save to database or encrypted storage
    pass
    
def debug_mode(request):

    return JsonResponse({'success': False, 'error': 'Forbidden', 'message': 'You do not have permission for access this resource'}, status = 403)
    # For testing only
    try:
        from .tasks import schedule_algo, schedule_stream_worker
        schedule_algo.delay()
        schedule_stream_worker()
        return JsonResponse({'success': True}, status=200)
    except Exception as a:
        return JsonResponse({'success': False, 'message': f'Error : {a}'}, status=400)