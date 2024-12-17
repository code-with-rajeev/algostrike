"""
Description :

"""
from django.http import JsonResponse
from broker_utils import *
# importing required_credentials, does_broker_exist, route_broker, get_credentials

def authenticate(credentials):

    # check for missing credentials !
    response = requried_credentials(credentials)
    if (not response.success):
        return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)
    
    # check whether, broker is already registered. No need to store credentials in database. Update logs and session after authenticating successfully. 
    response = does_broker_exist(credentials)
    if (not response.success):
        # optional: If already exits, try to renew session/ login-again. Avoid data redudancy.
        return JsonResponse({'success': False, 'message': 'Broker already exist'}, status=400)

    #  route broker's credentials to their appropriate authentication / login method
    response = route_broker(credentials)
    if (not response.success):
        """
        return response
        """
        message = 'Invalid Credentials' # Temporary response
        return JsonResponse({'success': False, 'message': message}, status=400)
        
    