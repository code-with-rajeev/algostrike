from neo_api_client import NeoAPI

"""
Credentials
"""
consumer_key = ''
consumer_secret = ''


"""
Handle sockets

def on_message(message):
    pass
    
def on_error(error_message):
    pass
"""

def make_connection():
    client = NeoAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, environment='prod',
                access_token=None, neo_fin_key=None)
    #Set socket listener

    """
    client.on_message = on_message
    client.on_error = on_error
    """
    client.login(mobilenumber=" ", password=" ")

    client.session_2fa(OTP=" ")
    return client

make_connection()