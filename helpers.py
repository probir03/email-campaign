from flask import Flask, request, url_for
import bcrypt, uuid, random, requests
import datetime, time
from app import app

def datetime_to_epoch(date):
    return time.mktime(date.timetuple())*1000
'''
To create url for pagination 
'''
def url_for_other_page(page):
    args = dict(request.args)
    args['page'] = page
    return url_for(request.endpoint, _external=True, **args)

'''
To hash the password
'''
def hash_password(password):
    return bcrypt.hashpw(str(password), bcrypt.gensalt())

'''
To hash the access-token
'''
def access_token():
    return bcrypt.hashpw(str(random.random()), bcrypt.gensalt())

'''
To validate/comapre the hash password
@param present - user's account present password
@param requested - password requested for verification
'''
def validate_hash_password(requested, present):
    return bcrypt.checkpw(str(requested), str(present))

'''
To generate unique code
uuid package
'''
def generate_unique_code():
    return uuid.uuid4().__str__()

'''
error message
'''
def error(message):
    return {
        'message' : message, 
        'tags' : 'error'
    }

'''
Get redirect function 
'''
def get_redirect_resolver(provider):
    if provider == 'google':
        return 'google_redirect'
    if provider == 'facebook':
        return 'facebook_redirect'
    if provider == 'github':
        return 'github_redirect'

'''
get authrization function
'''
def get_authrize_resolver(provider):
    if provider == 'google':
        return 'google_authorize'
    if provider == 'facebook':
        return 'facebook_authorize'
    if provider == 'github':
        return 'github_authorize'

'''
modify an url
'''
def modify_url(url):
    local_url = get_local_server_url().split("//")[-1]
    return url.replace(url.split("//")[-1].split("/")[0], local_url)

'''
get respective api server url
'''
def get_local_server_url():
    if app.config['APP_ENV'] == 'local':
        return "http://10537e68.ngrok.io"
    return "http://localhost:5000"

'''
get feedr url
'''
def get_feedr_url():
    if app.config['APP_ENV'] == 'production':
        return "http://139.59.4.41/"
    return "http://localhost:8000"

'''
success message
'''
def success(message):
    return {
        'message' : message, 
        'tags' : 'success'
    }