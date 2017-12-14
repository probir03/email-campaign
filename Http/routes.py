from flask import Blueprint, render_template

router = Blueprint("admin_route",  __name__, template_folder='Auth.templates')

@router.route("/")
def home():
	return render_template('admin_login.html')