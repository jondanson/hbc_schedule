from flask import Blueprint, request, session, url_for, render_template
from src.models.events.events import Event
from werkzeug.utils import redirect
# import src.models.members.errors as EventErrors
from src.models.members.members import Member

# import src.models.admin.decorators as admin_decorators

event_blueprint = Blueprint('events', __name__)


@event_blueprint.route('/index_of_events')
def index_of_events():
    events = Event.all()
    event1 = []
    for event in events:
        member_ids = event.assigned_members
        for member_id in member_ids:
            member = Member.find_by_id(member_id)
            member_name = member.first_name + " " + member.last_name
            event.assigned_members[event.assigned_members.index(member_id)] = member_name

        event1.append(event)

    return render_template('events/events_index.jinja2', events=event1)


@event_blueprint.route('/new_event', methods=['GET', 'Post'])
# @admin_decorators.requires_admin_permissions
def create_event():
    members = Member.all_sorted()
    if request.method == 'POST':
        title = request.form['title']
        day_of_event = request.form['day_of_event']
        ministry = request.form['ministry']
        assigned_members = request.form.getlist('assigned_members')
        member_ids = []

        for member in assigned_members:
            member_id = member.split()[-1]
            member_ids.extend([member_id])

        Event(title, day_of_event, ministry, member_ids).save_to_mongo()

        return redirect(url_for('.index_of_events'))

    return render_template('events/create_event.jinja2', members=members)


@event_blueprint.route('/edit/<string:event_id>', methods=['GET', 'POST'])
# @admin_decorators.requires_admin_permissions
def edit_event(event_id):
    event = Event.find_by_id(event_id)
    members = Member.all_sorted()
    if request.method == 'POST':
        title = request.form['title']
        day_of_event = request.form['day_of_event']
        ministry = request.form['ministry']
        assigned_members = request.form.getlist('assigned_members')
        member_ids = []

        for member in assigned_members:
            member_id = member.split()[-1]
            member_ids.extend([member_id])

        for this in event:
            this.title = title
            this.day_of_event = day_of_event
            this.ministry = ministry
            this.assigned_members = member_ids

            this.save_to_mongo()

        return redirect(url_for('.index_of_events'))
    return render_template('events/edit_event.jinja2', event=event, members=members)

@event_blueprint.route('/delete/<string:event_id>')
#@admin_decorators.check_login
def delete_event(event_id):
    events = Event.find_by_id(event_id)
    for event in events:
        event.delete()
    return redirect(url_for('.index_of_events'))