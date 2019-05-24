# coding=utf-8


"""
数据库模型
"""
from . import db
from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash


class Moment(Enum):
    """
    枚举时段
    """
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    NIGHT = "Night"


class End_tpye(Enum):
    """
    结束类型
    """
    KNOWN = "Known"
    USEABLE = "Useable"
    PROFICIENT = "Proficient"
    COMPREHEND = "omprehend"


class BaseModel(object):
    """
    基类，提供数据库更新时间字段
    """
    timestamp = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


class User(BaseModel, db.Model):
    """
    用户模型类
    """
    __tablename__ = "Users"

    user_id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=True)
    last_login = db.Column(db.DateTime, nullable=False)

    # 将密码加密存储
    @property
    def password(self):
        """设置外部无法访问"""
        raise AttributeError("当前属性不允许读取")

    @password.setter
    def password(self, value):
        """对密码进行加密"""
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        """校验密码"""
        return check_password_hash(self.password_hash, password)


class Profession(BaseModel, db.Model):
    """
    专业类
    """
    __tablename__ = "professions"

    prof_id = db.Column(db.Integer, primary_key=True)
    prof_name = db.Column(db.String(64), unique=True, nullable=False)
    major_or_not = db.Column(db.Boolean, default=True, nullable=False)
    target = db.relationship("Target", backref="Profession", lazy="dynamic")
    user_id = db.Column(db.BigInteger, db.ForeignKey("Users.user_id"))

    def __repr__(self):
        return "professions:%s" % self.prof_name


class Target(BaseModel, db.Model):
    """
    目标类
    """
    __tablename__ = "targets"

    tg_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Date, nullable=False)
    end_time = db.Column(db.Date, nullable=False)
    end_sign = db.Column(db.String(128), nullable=False)
    tg_end_status = db.Column(db.Enum(End_tpye), default="Known", nullable=False)
    tg_name = db.Column(db.String(64), unique=True, nullable=False)
    prof_id = db.Column(db.Integer, db.ForeignKey("professions.prof_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    plan = db.relationship("Plan", backref="Target", lazy="dynamic")

    def __repr__(self):
        return "targets:%s" % self.tg_name


class Todo_list(BaseModel, db.Model):
    """
    代办列表
    """
    __tablename__ = "todo_lists"

    td_id = db.Column(db.Integer, primary_key=True)
    read = db.Column(db.String(128), nullable=True)
    watch = db.Column(db.String(128), nullable=True)
    expression = db.Column(db.String(128), nullable=True)
    practice = db.Column(db.String(128), nullable=True)
    community = db.Column(db.String(128), nullable=True)
    pl_id = db.Column(db.Integer, db.ForeignKey("plans.pl_id"))


class Plan(BaseModel, db.Model):
    """
    计划类
    """
    __tablename__ = "plans"

    # 计划字段
    pl_id = db.Column(db.Integer, primary_key=True)
    pl_name = db.Column(db.String(128), nullable=False)
    tg_name = db.Column(db.String(128), nullable=False)
    pl_date = db.Column(db.Date, nullable=False)
    pl_moment = db.Column(db.Enum(Moment), nullable=False)
    pl_end_status = db.Column(db.Enum(End_tpye), default="Known", nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    tg_id = db.Column(db.Integer, db.ForeignKey("targets.tg_id"))

    # 计划反馈字段
    fb_status = db.Column(db.Enum(End_tpye), default=None, nullable=True)
    fb_text = db.Column(db.TEXT, default=None, nullable=True)
    comp_percent = db.Column(db.Float, default=None, nullable=True)
    todo_list = db.relationship("Todo_list", backref="Plan", lazy="dynamic")

    def __repr__(self):
        return "plans:%s" % self.pl_name
