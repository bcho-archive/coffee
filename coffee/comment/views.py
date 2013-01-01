#coding: utf-8

from flask import Blueprint, render_template, redirect, url_for, abort, \
                  request, g

from coffee.db import db
from coffee.models import Comment

from coffee.user.utils import require_admin
from .utils import find_author


app = Blueprint('comment', __name__, template_folder='templates')


@app.route('/', methods=['GET'])
def view_comment():
    comments = db.query(Comment)
    find_author(comments)
    return render_template('comments.html', comments=comments)


@app.route('/add', methods=['POST'])
def add_comment():
    content = request.form['content']
    comment = Comment().create(content, g.user)
    db.add(comment)
    db.commit()

    return redirect(url_for('.view_comment'))


@app.route('/<int:id>/del', methods=['GET'])
@require_admin
def delete_comment(id):
    comment = db.query(Comment, condition=lambda x: x['id'] == id, count=1)
    if not comment:
        abort(404)
    else:
        db.remove(comment[0])
        db.commit()
        return redirect(url_for('.view_comment'))


@app.route('/<int:refer_id>/reply', methods=['POST'])
def reply_comment(refer_id):
    content = request.form['content']
    comment = Comment().create(content, g.user)
    comment['refer'] = refer_id
    db.add(comment)
    db.commit()

    return redirect(url_for('.view_comment'))
