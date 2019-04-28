# coding=utf-8


"""
数据库模型
"""
from Aum_water.start import db


class Role(db.Model):
    """
    角色模型
    """

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    us = db.relationship("User", backref='role')

    def __repr__(self):
        return "Role:%s" % self.name


class User(db.Model):
    """
    用户模型
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User:%s' % self.name
