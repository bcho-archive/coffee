#coding: utf-8

from coffee.db import db
from coffee.models import User, Comment


def find_author(comments):
    for comment in comments:
        u = db.query(User, lambda x: x['id'] == comment['author_id'])
        comment['author'] = u[0] if u else None


def find_reference(comments):
    for comment in comments:
        u = db.query(Comment, lambda x: x['id'] == comment['refer_id'])
        comment['refer'] = u[0] if u else None
