from app import app, db

from Http.routes import router
from Auth.routes import auth
from drip.routes import drip

app.register_blueprint(router)
app.register_blueprint(auth)
app.register_blueprint(drip)

if __name__=='__main__':
	app.run(debug=True)