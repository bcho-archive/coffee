#coding: utf-8

from flask import Blueprint, render_template, request, redirect, \
                  url_for

from coffee.db import db
from coffee.models import User
from coffee.utils import encrypt
from .utils import require_login, login, logout

app = Blueprint('user', __name__, template_folder='templates')


@app.route('/', methods=['GET'])
@require_login
def users_view():
    users = db.query(User)
    return render_template('users.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        name = request.form.get('name', None)
        password = encrypt(request.form.get('password', ''))
        u = db.query(User, condition=lambda x: x['name'] == name)
        if not u:
            #: TODO flash message
            return redirect(url_for('.user_login'))
        else:
            u = u[0]
            if u['password'] == password:
                u.generate_token()
                login(u)
                next = request.args.get('next', None)
                if next:
                    return redirect(next)
                else:
                    return redirect(url_for('.users_view'))
            else:
                #: TODO flash message
                return redirect(url_for('.user_login'))
    return redirect(url_for('.user_login'))


@app.route('/logout', methods=['GET', 'POST'])
@require_login
def user_logout():
    logout()
    next = request.args.get('next', None)
    if next:
        return redirect(next)
    return redirect(url_for('.user_login'))
