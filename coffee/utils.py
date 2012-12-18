#coding: utf-8

import os
from datetime import datetime
import sha

from config import project_codename, data_path, datetime_format, salt


def import_object(name, arg=None):
    if '.' not in name:
        return __import__(name)
    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    return getattr(obj, parts[-1], arg)


def register_blueprint(app, blueprint):
    url_prefix = '/%s' % blueprint
    views = import_object('%s.%s.views' % (project_codename, blueprint))
    app.register_blueprint(views.app, url_prefix=url_prefix)
    return app


def build_datapath(pathname):
    '''Build the full data path.'''
    return os.path.join(data_path, pathname)


def utc_now():
    return datetime.strftime(datetime.utcnow(), datetime_format)


def encrypt(p):
    return sha.sha(salt + p).hexdigest()
