from flask import Blueprint, render_template

router = Blueprint("admin_route",  __name__, template_folder='Auth.templates')

@router.route("/")
def list_drips():
	return render_template('admin_login.html')