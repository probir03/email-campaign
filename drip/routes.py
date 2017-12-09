from flask import Blueprint, render_template, request, redirect 
from App.Response import *
from decorator import login_required
import views


drip = Blueprint("drip_route",  __name__, template_folder='templates')

@drip.route('/drip/create', methods=['GET'])
@login_required
def crete_drip():
	return render_template('create_drip.html')

@drip.route('/drips', methods=['GET', 'POST'])
@login_required
def dashboard():
	if request.method == 'GET':
		response = views.list()
		return render_template('dashboard.html', drips = response)
	resonse = views.create_drip(request)
	return redirect('/drips')

@drip.route('/drips/<drip_id>', methods=['GET', 'PUT'])
@login_required
def get_drip(drip_id):
	if request.method == 'GET':
		response = views.get_by_id(drip_id)
		print response
		return render_template('drip.html', drip = response)
	resonse = views.create_drip(request)
	return redirect('/drips')

@drip.route('/drips/<drip_id>/emails', methods=['POST'])
@login_required
def attach_email(drip_id):
	response = views.attach_recipent(request, drip_id)
	return redirect('/drips/'+drip_id)