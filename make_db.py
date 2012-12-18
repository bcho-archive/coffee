#coding: utf-8

from coffee.db import db 
from coffee.models import User
from coffee.config import visitor, role


def create_visitor():
    v = User().create(**visitor)
    db.add(v)
    db.commit()


def create_admin():
    v = User().create('admin', 'secret', role['admin'])
    db.add(v)
    db.commit()


def main():
    create_admin()
    create_visitor()


if __name__ == '__main__':
    main()
