from flask import Blueprint, request, session, url_for, render_template
from src.models.members.members import Member
from werkzeug.utils import redirect
import src.models.members.errors as MemberErrors
import src.models.members.decorators as members_decorators
member_blueprint = Blueprint('members', __name__)


@member_blueprint.route('/member_register', methods=['GET', 'POST'])
def register_member():
    if request.method == 'POST':
        # Check Login is valid
        name = request.form['name']
        email = request.form['email']
        cell_phone = request.form['cell_phone']


        try:
            if User.register_user(name, email, cell_phone):
                return redirect(url_for('.members_list'))
        except MemberErrors.MemberError as e:
            return e.message

    return render_template('members/register.jinja2')
