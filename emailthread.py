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

import models
from oauth2client.client import Credentials
users = models.User.query.filter_by(email='probir@sourceeasy.com').all()
for user in users:
	if not user.credentials:
		print user.email, " No user creds"
		continue
	print user.email, "Running"
	credentials = Credentials.new_from_json(user.credentials)
	thread_list = user.message_thread
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)
	print "service created"
	print thread_list
	for id in thread_list:
		tdata = service.users().threads().get(userId=user.email, id=id).execute()
		# print "zdsd", tdata['messages'][0]['payload']['headers'][0]['value']
		nmsgs = len(tdata['messages'])
		# break
		print nmsgs, tdata['messages']
		if nmsgs > 0:    # skip if <3 msgs in thread
			msg = tdata['messages'][0]['payload']
			subject = ''
			for header in msg['headers']:
				if header['name'] == 'Subject':
					subject = header['value']
					break
			if subject:  # skip if no Subject line
				print('- %s (%d msgs)' % (subject, nmsgs))
		break
	break