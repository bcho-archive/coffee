#coding: utf-8

from flask import Flask, g, redirect, url_for

from utils import register_blueprint
from config import blueprints, project_codename
from user.utils import get_current_user


#: init app
app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.before_request
def init():
    g.project_codename = project_codename
    g.user = get_current_user()


#: register blueprints
for blueprint in blueprints:
    register_blueprint(app, blueprint)


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('comment.view_comment'))
