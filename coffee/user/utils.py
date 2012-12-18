#coding: utf-8

from flask import g, abort, session
import functools

from coffee.config import role
from coffee.db import db
from coffee.models import User


visitor = db.query(User, lambda x: x['role'] == role['visitor'])[0]


#: TODO factory builder
def require_login(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if g.user['role'] > role['visitor']:
            return func(*args, **kwargs)
        else:
            abort(403)
    return wrapper


def require_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if g.user['role'] == role['admin']:
            return func(*args, **kwargs)
        else:
            abort(403)
    return wrapper


def login(user):
    if not user:
        return
    session['id'] = user['id']
    session['token'] = user['token']
    session.permanent = True


def logout():
    if 'id' not in session:
        return
    session.pop('id')
    session.pop('token')


def get_current_user():
    if 'id' not in session or 'token' not in session:
        return visitor
    u = db.query(User, lambda x: x['id'] == session['id'])
    if u and u[0]['token'] == session['token']:
        return u[0]
    return visitor
