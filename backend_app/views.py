from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Disable CSRF for simplicity (only in development)
def broker_credentials(request):
    
    if request.method == 'POST':
        try:
            # temporarily redirect under maintainance response
            return JsonResponse({'success': False, 'message': 'This service is under maintainance, Please try again later!'}, status=401)

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
    global mobile_number
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            otp = data.get('otp')

            # Validate input
            if not all([otp, mobile_number]):
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
                    print(f"Storing credentials for {mobile_number} credentials")

                    # Clear temporary cache
                    # cache.delete(cache_key)

                    return JsonResponse({'success': True, 'message': 'Broker added successfully'})
                else:
                    return JsonResponse({'success': False, 'message': 'Temporary credentials not found'}, status=404)
            else:
                return JsonResponse({'success': False, 'message': 'Invalid OTP'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


def store_credentials(customer_key, customer_secret, password, mobile_number):
    # Simulate storing credentials (replace with actual database or secure storage logic)
    print(f"Storing credentials: {customer_key}, {customer_secret}, {password}, {mobile_number}")
    # Example: Save to database or encrypted storage
    pass
