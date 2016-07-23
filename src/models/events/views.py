import json
from flask import Blueprint, render_template, request, redirect, url_for
from src.models.events.events import Events
import src.models.user.decorators as user_decorators

event_blueprint = Blueprint('events', __name__)


@event_blueprint.route('/')
def index():
    events = Events.all()
    return render_template('events/events_index.jinja2', events=events)
