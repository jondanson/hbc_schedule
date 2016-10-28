from flask import Flask, render_template
from src.common.database import Database


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.jinja2')


from src.models.members.views import member_blueprint
from src.models.admin.views import admin_blueprint
from src.models.events.views import event_blueprint
app.register_blueprint(member_blueprint, url_prefix="/members")
app.register_blueprint(admin_blueprint, url_prefix="/admins")
app.register_blueprint(event_blueprint, url_prefix="/events")

