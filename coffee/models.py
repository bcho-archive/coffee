#coding: utf-8

import json
import os

import config
from utils import build_datapath, utc_now, encrypt


class FileModel(object):
    '''Store the data as file.'''

    name = None
    data_path = None
    keys = []

    def __init__(self):
        self._data = {}

    def __getitem__(self, name):
        return self._data.get(name, None)

    def __setitem__(self, name, val):
        self._data[name] = val

    def get(self, k, default):
        return self._data.get(k, default)

    def create(self):
        '''Build from scratch.'''
        raise NotImplementedError

    @staticmethod
    def fromdict(d):
        '''Build obj from a dict.'''
        raise NotImplementedError

    def validate(self, key, value):
        return self.get(key, None) == value

    @property
    def path(self):
        return os.path.join(self.data_path, '%s.txt' % (str(self['id'])))

    @property
    def data(self):
        '''Jsonify the data.'''
        d = {}
        for i in self.keys:
            d[i] = self[i]
        return json.dumps(d)

    def save(self):
        '''Save the data to `data_path/id.txt`.'''
        f = open(self.path, 'w')
        f.write(self.data)
        f.close()

    def delete(self):
        '''Delete from the disk.'''
        os.remove(self.path)


class Comment(FileModel):

    name = 'comments'
    data_path = build_datapath(name)
    keys = ['id', 'content', 'created_time', 'author_id', 'refer_id']

    def create(self, content, author):
        self['content'] = content
        self['author_id'] = author['id']
        self['created_time'] = utc_now()
        self['refer_id'] = None
        return self

    @staticmethod
    def fromdict(d):
        o = Comment()
        for key in o.keys:
            o[key] = d.get(key, None)
        return o

    def __repr__(self):
        return '<Comment %s(%d %d)>' % (self['content'].encode('utf-8'),
                                        self['id'], self['author_id'])


class User(FileModel):

    name = 'users'
    data_path = build_datapath(name)
    keys = ['id', 'name', 'password', 'role', 'token']

    def create(self, name, raw_password, role):
        self['name'] = name
        self['password'] = encrypt(raw_password)
        self['role'] = role
        self['token'] = ''
        return self

    @staticmethod
    def fromdict(d):
        o = User()
        for key in o.keys:
            o[key] = d.get(key, None)
        return o

    def __repr__(self):
        return '<User %s(%d %d)>' % (self['name'].encode('utf-8'), self['id'],
                                     self['role'])

    def generate_token(self):
        self['token'] = encrypt('%s%s%s' % (
                                self['name'], self['password'], utc_now()))
        self.save()
        return self['token']

    @property
    def role(self):
        for k, v in config.role.items():
            if self['role'] == v:
                return k
        return None
