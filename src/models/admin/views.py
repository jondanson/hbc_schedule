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
                return redirect(url_for('.admin_home.jinja2'))#todo: fix home page to show scheduling info and options if logged.
        except AdminErrors.AdminNotExistError as e:
            return e.message

    return render_template('admin/login.jinja2')
