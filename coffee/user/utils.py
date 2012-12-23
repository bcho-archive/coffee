#coding: utf-8

from flask import g, abort, session
import functools

from coffee.config import role
from coffee.db import db
from coffee.models import User


visitor = db.query(User, lambda x: x['role'] == role['visitor'])[0]


class require_role(object):
    '''Create a function decorator which requires user's role
    higher than given role.
    '''
    def __init__(self, role):
        self.role = role

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if g.user['role'] > self.role:
                return func(*args, **kwargs)
            else:
                #: raise redirect rather than abort with 403
                abort(403)
        return wrapper


require_login = require_role(role['visitor'])
require_admin = require_role(role['visitor'])


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
