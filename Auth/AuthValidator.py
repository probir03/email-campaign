from flask import Flask
from AuthRepository import AuthRepository
from models import User

def create_user_rule(inputs):
	if 'email' in inputs and 'password' in inputs and 'displayName' in inputs and 'rePassword' in inputs :
		existing_user = AuthRepository().filter_attribute(User, {'email': inputs['email']})
		if existing_user:
			raise Exception('Email already Exists', 422)
		if inputs['password'] == inputs['rePassword'] : 
			return True
	raise Exception('Invalid Inputs', 422)
