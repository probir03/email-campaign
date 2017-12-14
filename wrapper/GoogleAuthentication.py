from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from flask import redirect
import requests, json, helpers
from app import app
from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
from oauth2client.client import FlowExchangeError
from apiclient.discovery import build
import logging, flask
import google_auth_oauthlib
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests


CLIENTSECRETS_LOCATION = 'client_secret_worker.json'
REDIRECT_URI = helpers.get_local_server_url()+"/app/auth?provider=google"

# (Receive token by HTTPS POST)
# ...
def googleDefaults():
    default = {}
    default['token_request_uri'] = "https://accounts.google.com/o/oauth2/auth"
    default['response_type'] = "code"
    default['user_redirect_uri'] = helpers.get_local_server_url()+"/app/auth?provider=google"
    default['scope'] = "https://mail.google.com/+https://www.googleapis.com/auth/userinfo.email+https://www.googleapis.com/auth/userinfo.profile"
    default['login_failed_url'] = '/'
    default['access_token_uri'] = 'https://accounts.google.com/o/oauth2/token'
    default['grant_type'] = 'authorization_code'
    return default


def redirectTo():
    url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&access_type=offline&prompt=consent".format(
        token_request_uri = googleDefaults()['token_request_uri'],
        response_type = googleDefaults()['response_type'],
        client_id = app.config['GOOGLE_CLIENT_ID'],
        redirect_uri = googleDefaults()['user_redirect_uri'],
        scope = googleDefaults()['scope'],
        access_type = 'offline',
        )
    return redirect(url)

def exchange_code(authorization_code):
    """Exchange an authorization code for OAuth 2.0 credentials.

    Args:
    authorization_code: Authorization code to exchange for OAuth 2.0
                        credentials.
    Returns:
    oauth2client.client.OAuth2Credentials instance.
    Raises:
    CodeExchangeException: an error occurred.
    """
    flow = flow_from_clientsecrets(CLIENTSECRETS_LOCATION, ' '.join(googleDefaults()['scope'].split(' ')))
    flow.redirect_uri = googleDefaults()['user_redirect_uri']
    try:
        credentials = flow.step2_exchange(authorization_code)
        # credentials = flow.crsedentials
        return credentials
    except FlowExchangeError, error:
        logging.error('An error occurred: %s', error)
        raise Exception(error)

# To Authorize the user with google signin
def authorize(request):
    import json
    creds = exchange_code(request.args.get('code'))
    return json.loads(creds.to_json())['token_response']['access_token'], creds

#getting user Details
def get_user_details(token):
    headers = {
        'Authorization': 'Bearer '+token
    }
    user_info = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
    user_info = json.loads(user_info.content)
    if 'email' not in user_info:
        raise Exception("invalid google auth token")
    return create_user_data(user_info)

#user data to store in database
def create_user_data(user_info):
    print user_info
    if 'verified_email' in user_info and bool(user_info['verified_email']) is not True:
        raise Exception('Email is not verified')
    elif 'email_verified' in user_info and bool(user_info['email_verified']) is not True:
        raise Exception('Email is not verified')
    return {
        'email' : user_info['email'],
        'display_name' : user_info['email'].split('@')[0],
        'first_name' : user_info['name'].split(' ')[0],
        'last_name' : user_info['family_name'],
        'logo' :  user_info['picture'] if 'picture' in user_info else None
    }