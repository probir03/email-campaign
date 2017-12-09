from flask import Flask, Blueprint, request, session
from flask import render_template, jsonify
from views import *
from decorator import login_required

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/app/signin', methods=['GET'])
def signin():
    return social_signin(request.args.get('provider'))

@auth.route('/app/auth', methods=['GET'])
def app_auth():
    response = social_app_login(request)
    return redirect('/drips')
    
@auth.route('/app/logout', methods=['GET'])
@login_required
def app_logout():
    response = logout()
    return response
