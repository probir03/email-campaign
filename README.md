# email-campaign-
Create env.py file and add keys

	APP_ENV = 'local'

	DEBUG = True/Flase

	SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/<database_name>'

	SQLALCHEMY_TRACK_MODIFICATIONS = False

	SECRET_KEY='yuiop3fcvbnoiuy4hgfdc4vbnbvcx23456vbnmkjhgf3456bnmkjhc34'

	GOOGLE_CLIENT_ID='google client id'

	GOOGLE_CLIENT_SECRET='secret key'

Run Command
	```
	$ pip install -r requirements.txt

	$ python manage.py db upgrade

	$ python manage.py runserver
	```

Download and save project client_secret.json in root directory

set in crontab or use supervisor
	```
	python worker.py

	celery worker -A EmailJob.email_manager.celery

	```
	
