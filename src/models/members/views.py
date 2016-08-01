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
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        cell_phone = request.form['cell_phone']


        try:
            if Member.register_member(first_name, last_name, email, cell_phone):
                return redirect(url_for('members.index'))
        except MemberErrors.MemberError as e:
            return e.message

    return render_template('members/register.jinja2')

@member_blueprint.route('/')
def index():
    members = Member.all_sorted()
    return render_template('members/member_list.jinja2', members=members)