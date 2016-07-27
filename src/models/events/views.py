import json
from flask import Blueprint, render_template, request, redirect, url_for
from src.models.events.events import Event
import src.models.events.decorators as event_decorators

event_blueprint = Blueprint('events', __name__)


@event_blueprint.route('/index')
def index():
    events = Event.all()
    return render_template('events/events_index.jinja2', events=events)


@event_blueprint.route('/new', methods=['GET', 'Post'])
#@event_decorators.requires_admin_permissions
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        day_of_event = request.form['day_of_event']
        tag = request.form['tag']
        assigned_members = request.form['assigned_members']

        Event(title, day_of_event, tag, assigned_members).save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('events/create_event.jinja2')

@event_blueprint.route('/edit/<string:_id>', methods=['GET', 'POST'])
#@event_decorators.requires_admin_permissions
def edit_event(_id):
    event = Event.find_by_id(_id)
    if request.method == 'POST':
        title = request.form['title']
        day_of_event = request.form['day_of_event']
        tag = request.form['tag']
        assigned_members = request.form['assigned_members']
        active = request.form['active']

        event.title = title
        event.day_of_event = day_of_event
        event.tag = tag
        event.assigned_members = assigned_members
        event.active = active

        event.save_to_mongo()

        return redirect(url_for('.index'))
    return render_template('events/edit_event.jinja2', event=event)