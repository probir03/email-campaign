from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('env.py')

db = SQLAlchemy(app)

from Http.routes import router
from Auth.routes import auth
from drip.routes import drip

app.register_blueprint(router)
app.register_blueprint(auth)
app.register_blueprint(drip)

if __name__=='__main__':
	app.run(debug=True)

	