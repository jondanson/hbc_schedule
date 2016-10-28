from flask import Blueprint, request, session, url_for, render_template
from src.models.admin.admin import Admin
from werkzeug.utils import redirect
import src.models.admin.errors as AdminErrors
#import src.models.admin.decorators as admin_decorators
admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        # Check Login is valid
        email = request.form['email']
        password = request.form['password']

        try:
            if Admin.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('home'))
        except AdminErrors.AdminNotExistError as e:
            return e.message
    print (request.remote_addr)
    return render_template('admin/login.jinja2')

@admin_blueprint.route('/logout', methods=['GET'])
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))