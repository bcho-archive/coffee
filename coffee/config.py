#coding: utf-8

import os


#: basic config
project_codename = 'coffee'
SECRET_KEY = 'coffee'
#: FIXME tricky relative path
data_path = os.path.abspath('data')
datetime_format = '%Y %m %d %H:%M:%S'
salt = project_codename

#: role settings
role_list = ['visitor', 'admin']
role = {}
for i, name in enumerate(role_list):
    role[name] = 1 << i

visitor = {
    'name': u'游客',
    'raw_password': '12345',
    'role': role['visitor'],
}

#: enabled blueprints
blueprints = ['user', 'comment']

#: debug
DEBUG = True
