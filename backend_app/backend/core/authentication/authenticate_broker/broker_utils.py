"""
Helper / neccessary functions that may be used while authentication / login / other process
"""
def requried_credentials(credentials):
    
    # Temporarily redirect under maintainance response
    return JsonResponse({'success': False, 'message': 'This service is under maintainance, Please try again later!'}, status=401)

def does_broker_exist(credentials):
    message = 'Some error occured' # Temporary response to avoid further processing
    return JsonResponse({'success': False, 'message': message}, status=400)

def route_broker(credentials):
    message = 'Some error occured' # Temporary response to avoid further processing
    return JsonResponse({'success': False, 'message': message}, status=400)