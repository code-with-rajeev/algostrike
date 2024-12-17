"""
Helper / neccessary functions that may be used while authentication / login / other process
"""
def requried_credentials(credentials):
    
    # Test: Bypass missing credentials check
    if credentials.get('API Key') == 'missing_credentials':
        return {'success': False, 'message': 'Missing Fields Required', 'status':400}
    return {'success': True}

def does_broker_exist(credentials):
    # Test: Bypass duplicate broker's credentials check
    if credentials.get('API Key') == 'existing_credentials':
        return {'success': False, 'message': "Broker's credentials already exist", 'status':400}
    return {'success': True}

def route_broker(credentials):
    if credentials.get('API Key') == 'invalid_credentials':
        return {'success': False, 'message': 'Invalid Credentials', 'status':400}
    return {'success': True}

"""
When service is unavailable
return {'success': False, 'message': 'This service is under maintainance, Please try again later!', 'status':503}
"""