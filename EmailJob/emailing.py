import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from oauth2client.file import Storage

def execute(service, user_id, message):
	try:
		message = (service.users().messages().send(userId=user_id, body=message).execute())
		return message
	except errors.HttpError, error:
		return "Error"

def send_message(sender, to, subject, msgHtml, msgPlain=''):
	import models
	from oauth2client.client import Credentials
	user = models.User.query.filter_by(email=sender).first()
	if not user.credentials:
		print "No user creds"
		return
	credentials = Credentials.new_from_json(user.credentials)
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = to
	msg.attach(MIMEText(msgPlain, 'plain'))
	msg.attach(MIMEText(msgHtml, 'html'))
	message = {'raw': base64.urlsafe_b64encode(msg.as_string())}

	return execute(service, sender, message)

