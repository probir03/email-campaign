import models
import jinja2, pickle
import emailing, json
from app import db, app
from celery import Celery

celery = Celery('worker', broker=app.config['broker_url'])
celery.conf.update(app.config)

class DripCampaign():

	def run(self):
		drips = models.Drip.query.filter_by(is_enabled=True, is_completed=False).all()
		print drips
		i = 1
		for drip in drips:
			self.run_campaign(drip)
			if i == 4:
				break
			i+=1
		print "worked"

	def run_campaign(self, drip):
		stage = drip.running_stage
		print stage
		if not stage:
			return
		for email in drip.recipient_list:
			drip.user
			drip.owner
			print "sending"
			DripCampaign.send_email_task.delay(pickle.dumps(drip), pickle.dumps(stage), email)

	@staticmethod
	@celery.task
	def send_email_task(drip, stage, email):
		print "came"
		drip = pickle.loads(drip)
		stage = pickle.loads(stage)
		owner = drip.owner
		message = owner.message_thread or []
		template = jinja2.Template(stage.template)
		var = stage.get_vars(email) or {}
		body = template.render(**var)
		response = emailing.send_message(drip.user.email, email, stage.subject, body)
		if response != 'Error':
			message.append(response['threadId'])
		print message, "fghjkjhg"
		owner.message_thread = message
		print "sffsfsfsds"
		print owner
		stage.is_sent = True
		db.session.add(stage)
		db.session.add(owner)
		db.session.commit()
		if not drip.next_stage:
			drip.is_completed = True
			db.session.add(drip)
			db.session.commit()
