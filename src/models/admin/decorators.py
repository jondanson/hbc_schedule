from src.config import ADMINS
from flask import session, url_for, redirect, request
from functools import wraps


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('admin.login_user', next=request.path))
        return func(*args, **kwargs)

    return decorated_function


def requires_admin_permissions(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('admin.login_user', next=request.path))
        if session['email'] not in ADMINS:
            return redirect(url_for('admin.login_user'))
        return func(*args, **kwargs)

    return decorated_function


def check_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('admin.login_user', next=request.path))
        return func(*args, **kwargs)

    return decorated_function