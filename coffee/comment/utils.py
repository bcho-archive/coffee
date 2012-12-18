#coding: utf-8

from coffee.db import db
from coffee.models import User


def find_author(comments):
    for comment in comments:
        u = db.query(User, lambda x: x['id'] == comment['author_id'])
        comment['author'] = u[0] if u else None
