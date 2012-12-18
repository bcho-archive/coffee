#coding: utf-8

import os
import json

from models import Comment, User


class QueryError(Exception):
    pass


class AddError(Exception):
    pass


class RemoveError(Exception):
    pass


class DB(object):
    '''Act as a db interface.'''

    def __init__(self, models):
        self.models = []
        self.data = {}
        for model in models:
            name = model.__name__
            self.models.append(model)
            self.data[name] = self._read_file(model)

    def _read_file(self, model):
        is_db_file = lambda x: os.path.splitext(x)[-1] == '.txt'

        objs = []
        for fname in os.listdir(model.data_path):
            full_path = os.path.join(model.data_path, fname)
            if os.path.isfile(full_path) and is_db_file(full_path):
                with open(full_path, 'r') as stream:
                    d = json.loads(stream.read())
                    objs.append(model.fromdict(d))
        objs.sort(key=lambda x: x['id'])
        return objs

    def _next_id(self, model_name):
        return max([i['id'] for i in self.data[model_name]] + [0]) + 1

    def query(self, model, condition):
        #: TODO improve condition (not only use lambda)
        if model not in self.models:
            raise QueryError
        if condition:
            return filter(condition, self.data[model.__name__])
        else:
            return self.data[model.__name__]

    def add(self, obj):
        if not any(map(lambda x: isinstance(obj, x), self.models)):
            raise AddError
        class_name = obj.__class__.__name__
        if obj not in self.data[class_name]:
            obj['id'] = self._next_id(class_name)
            self.data[class_name].append(obj)

    def remove(self, obj):
        if not any(map(lambda x: isinstance(obj, x), self.models)):
            raise RemoveError
        class_name = obj.__class__.__name__
        if obj not in self.data[class_name]:
            raise RemoveError
        else:
            self.data[class_name].remove(obj)
            obj.delete()

    def commit(self):
        for c in self.data.values():
            for i in c:
                i.save()


db = DB([Comment, User])
