from flask import Flask, session, flash 
from DripRepository import DripRepository
import models, helpers
from app import db
from dateutil import parser
from datetime import datetime
import csv

def list_drips():
	repo = DripRepository()
	return repo.fech_by_user(models.Drip, {'user_id' : session['user']['id']})

def create_drip(request):
	form_data = request.values
	data = {
		'id' : helpers.generate_unique_code(),
		'title' : form_data['title'],
		'user_id' : session['user']['id'],
		'description' : form_data['description'],
		'stage_number' : 0,
		'is_enabled' : False,
		'is_completed' : False
	}
	repo = DripRepository()
	return repo.store(models.Drip, data)

def get_by_id(id):
	repo = DripRepository()
	return repo.filter_attribute(models.Drip, {'id':id})

def enable_drip(id):
	drip = get_by_id(id)
	drip.is_enabled = True
	db.session.commit()
	return drip

def disable_drip(id):
	drip = get_by_id(id)
	drip.is_enabled = False
	db.session.commit()
	return drip

def attach_recipent(request, id, email=None):
	separator = ', '
	email = email or request.values.get('email')
	repo = DripRepository()
	drip = repo.filter_attribute(models.Drip, {'id':id})
	drip.recipient = drip.recipient + separator + email if drip.recipient else email
	drip.recipient = separator.join(list(set(drip.recipient.split(separator))))
	db.session.commit()
	return drip

def delete_recipent(id, email):
	drip = DripRepository().filter_attribute(models.Drip, {'id':id})
	drip.recipient = ','.join([x for x in drip.recipient.split(',') if x != email])
	db.session.commit()
	return drip

def add_stage(request, id):
	repo = DripRepository()
	drip = repo.filter_attribute(models.Drip, {'id':id})
	dt = parser.parse(request.values.get('date'))
	if drip.letast_stage is not None and drip.letast_stage.date > dt:
		flash('Please choose date after the previous stage')
	else:
		stage = repo.store(models.Stage, {
				'id' : helpers.generate_unique_code(),
				'name': request.values.get('name'),
				'subject': request.values.get('subject'),
				'date': request.values.get('date'),
				'template': request.values.get('templates'),
				'drip_id': drip.id,
			})
	return drip

def get_stage(request, drip_id, stage_id):
	repo = DripRepository()
	stage = repo.filter_attribute(models.Stage, {'id':stage_id, 'drip_id': drip_id}) 
	return stage

def update_stage(request, drip_id, stage_id):
	stage = get_stage(request, drip_id, stage_id)
	stage.name = request.values.get('name', stage.name)
	stage.subject = request.values.get('subject', stage.subject)
	stage.template = request.values.get('template', stage.template)
	stage.date = request.values.get('date', stage.date)
	db.session.commit()
	return stage

def update_vars(request, drip_id, stage_id, all=False):
	stage = get_stage(request, drip_id, stage_id)
	variables = {}
	for email in stage.drip.recipient_list:
		variables[email] = stage.get_vars(email) or {}
		if email == request.values.get('_user_email'):
			for var in stage.list_vars():
				variables[email][var] = request.values.get(var, stage.get_var(email, var))
	DripRepository().update(models.Stage, {'id': stage_id, 'drip_id': drip_id}, {'variables': variables})
	stage.variables = variables
	return stage

def update_vars_by_csv(request, drip_id, stage_id):
	stage = get_stage(request, drip_id, stage_id)
	email_list = stage.drip.recipient_list
	variables = {}
	csvfile = request.files.get('var_csv')
	reader = csv.DictReader(csvfile)
	variables = {}
	for row in reader:
		if row['email'] not in email_list:
			attach_recipent(request, stage.drip.id, row['email'])
		variables[row['email']] = {}
		for var in stage.list_vars():
			variables[row['email']][var] = row.get(var)
	stage.variables = variables
	db.session.commit()
	return stage




