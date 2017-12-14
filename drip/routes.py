from flask import Blueprint, render_template, request, redirect 
# from App.Response import *
from decorator import login_required
import views
import jinja2


drip = Blueprint("drip_route",  __name__, template_folder='templates')

@drip.route('/drip/create', methods=['GET'])
@login_required
def crete_drip():
	return render_template('create_drip.html')

@drip.route('/drips', methods=['GET', 'POST'])
@login_required
def dashboard():
	if request.method == 'GET':
		response = views.list_drips()
		return render_template('dashboard.html', drips = response)
	resonse = views.create_drip(request)
	return redirect('/drips')

@drip.route('/drips/<drip_id>', methods=['GET', 'PUT'])
@login_required
def get_drip(drip_id):
	if request.method == 'GET':
		response = views.get_by_id(drip_id)
		return render_template('drip.html', drip = response)
	resonse = views.create_drip(request)
	return redirect('/drips')

@drip.route('/drips/<drip_id>/enable', methods=['GET'])
@login_required
def enable_drip(drip_id):
	response = views.enable_drip(drip_id)
	return redirect('/drips/'+drip_id)

@drip.route('/drips/<drip_id>/disable', methods=['GET'])
@login_required
def disable_drip(drip_id):
	response = views.disable_drip(drip_id)
	return redirect('/drips/'+drip_id)

@drip.route('/drips/<drip_id>/emails', methods=['POST'])
@login_required
def attach_email(drip_id):
	response = views.attach_recipent(request, drip_id)
	return redirect('/drips/'+drip_id)

@drip.route('/drips/<drip_id>/emails/<email>', methods=['GET'])
@login_required
def delete_email(drip_id, email):
	response = views.delete_recipent(drip_id, email)
	return redirect('/drips/'+drip_id)

@drip.route('/drips/<drip_id>/stages', methods=['POST'])
@login_required
def add_stage(drip_id):
	response = views.add_stage(request, drip_id)
	return redirect('/drips/'+drip_id)

@drip.route('/drips/<drip_id>/stages/<stage_id>', methods=['GET', 'POST'])
@login_required
def update_stage(drip_id, stage_id):
	if request.method == 'POST':
		response = views.update_stage(request, drip_id, stage_id)
		return redirect('/drips/'+drip_id+'/stages/'+stage_id)
	else:
		stage = views.get_stage(request, drip_id, stage_id)
		return render_template("update_stage.html", stage=stage)

@drip.route('/drips/<drip_id>/stages/<stage_id>/view', methods=['GET'])
@login_required
def view_stage(drip_id, stage_id):
	stage = views.get_stage(request, drip_id, stage_id)
	template = jinja2.Template(stage.template)
	vars = stage.get_vars(request.args.get('email')) or {}
	return template.render(**vars)

@drip.route('/drips/<drip_id>/stages/<stage_id>/vars', methods=['POST'])
@login_required
def update_vars(drip_id, stage_id):
	stage = views.update_vars(request, drip_id, stage_id)
	return redirect('/drips/'+drip_id+'/stages/'+stage_id)

@drip.route('/drips/<drip_id>/stages/<stage_id>/vars/csv', methods=['POST'])
@login_required
def update_vars_by_csv(drip_id, stage_id):
	stage = views.update_vars_by_csv(request, drip_id, stage_id)
	return redirect('/drips/'+drip_id+'/stages/'+stage_id)

@drip.route('/google6352c900cb933b03.html')
def google_verification():
	return render_template('google6352c900cb933b03.html')