from flask import Flask, render_template, redirect, flash, url_for, session
from models import User
from Auth.AuthRepository import AuthRepository
import helpers, datetime, views
from Auth.AuthValidator import create_user_rule
from wrapper import GoogleAuthentication
from app import db

#create an user
def create_user(data):
	create_user_rule(data)
	repo = AuthRepository()
	inputs = {
		'id' : helpers.generate_unique_code().__str__(),
		'email' : data['email'],
		'password' : helpers.hash_password(data['password']), 
		'display_name' : data['displayName'],
		'logo' : data['logo'],
		'first_name' : data['firstName']\
			if 'firstName' in data else None,
		'last_name' : data['lastName']\
			if 'lastName' in data else None
	}
	user = repo.store(User, inputs)
	return user


def social_signin(provider):
	return getattr(views, helpers.get_redirect_resolver(provider))()

def google_redirect():
	return GoogleAuthentication.redirectTo()

def social_app_login(request):
	return getattr(views, helpers.get_authrize_resolver(request.args.get('provider')))(request)

def google_authorize(request):
	res, creds = GoogleAuthentication.authorize(request)
	return google_login(res, creds)

def google_login(token, creds):
	user_info = GoogleAuthentication.get_user_details(token)
	user = AuthRepository().filter_attribute(User, {'email' : user_info['email']})
	if user is None:
		data = {
			'email' : user_info['email'],
			'password' : None,
			'rePassword' : None,
			'displayName' : user_info['display_name'],
			'firstName' : user_info['first_name'],
			'lastName' : user_info['last_name'],
			'is_password_change_required' : False,
			'logo' : user_info['logo']
		}
		user = create_user(data)
	user.credentials = creds.to_json()
	db.session.commit()
	session['user'] = user.transform()
	return True

#Logout an user
def logout():
	del session['user']
	return redirect('/')
