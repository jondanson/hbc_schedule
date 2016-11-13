
from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
import src.models.admin.decorators as admin_decorators
import src.models.groups.groups as Groups

group_blueprint = Blueprint('groups', __name__)


@group_blueprint.route('/group_register', methods=['GET', 'POST'])
@admin_decorators.check_login
def register_group():
    if request.method == 'POST':
        # Check Login is valid
        group_name = request.form['group_name']
        assigned_members = request.form['assigned_members']


        try:
            if Groups.register_group(group_name, assigned_members):
                return redirect(url_for('members.index'))
        except MemberErrors.MemberError as e:
            return e.message

    return render_template('members/register.jinja2')