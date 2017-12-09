from flask import Flask, session 
from DripRepository import DripRepository
import models, helpers
from app import db

def list():
	repo = DripRepository()
	return repo.fech_by_user(models.Drip, {'user_id' : session['user']['id']})

def create_drip(request):
	form_data = request.values
	data = {
		'id' : helpers.generate_unique_code(),
		'title' : form_data['title'],
		'user_id' : session['user']['id'],
		'description' : form_data['description'],
		'stage_number' : 0
	}
	repo = DripRepository()
	return repo.store(models.Drip, data)

def get_by_id(id):
	repo = DripRepository()
	return repo.filter_attribute(models.Drip, {'id':id})

def attach_recipent(request, id):
	email = request.values.get('email')
	repo = DripRepository()
	drip = repo.filter_attribute(models.Drip, {'id':id})
	drip.recipient = drip.recipient + ', ' + email if drip.recipient else email
	db.session.commit()
	return drip