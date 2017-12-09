from flask import Flask, session, redirect

def login_required(func):
	def wraps(*args, **kwargs):
		if 'user' in session:
			return func(*args, **kwargs)
		return redirect('/')
	wraps.func_name = func.func_name
	return wraps