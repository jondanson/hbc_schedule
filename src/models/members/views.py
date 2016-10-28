from flask import Blueprint, request, session, url_for, render_template
from src.models.members.members import Member
from werkzeug.utils import redirect
import src.models.members.errors as MemberErrors
import src.models.admin.decorators as admin_decorators

member_blueprint = Blueprint('members', __name__)


@member_blueprint.route('/member_register', methods=['GET', 'POST'])
@admin_decorators.check_login
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
@admin_decorators.check_login
def index():
    members = Member.all_sorted()
    return render_template('members/member_list.jinja2', members=members)


@member_blueprint.route('/edit/<string:member_id>', methods=['GET', 'POST'])
@admin_decorators.check_login
def edit_member(member_id):
    member = Member.find_by_id(member_id)
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        cell_phone = request.form['cell_phone']

        member.first_name = first_name
        member.last_name = last_name
        member.email = email
        member.cell_phone = cell_phone
        member.save_to_mongo()

        return redirect(url_for('members.index'))
    return render_template('members/member_edit.jinja2', member=member)


@member_blueprint.route('/delete/<string:member_id>')
@admin_decorators.check_login
def delete_member(member_id):
    Member.find_by_id(member_id).delete()
    return redirect(url_for('members.index'))
