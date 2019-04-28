# coding=utf-8

from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from werkzeug.routing import BaseConverter
from flask import abort
from flask import Flask, make_response
from flask import session
from flask import current_app
from flask import g
from flask_script import Manager
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Response


# 自定义正则匹配路由
class RegexConverter(BaseConverter):
    """
    正则匹配路由
    """
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]

    def to_python(self, value):
        """
        
        :param value: 
        :return: 
        """
        return int(value)

    # def to_url(self, value):
    #     pass


class Config(object):
    """
    配置信息    
    """
    DEBUG = True

app = Flask(__name__)

app.secret_key = "tree"
app.url_map.converters["re"] = RegexConverter
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:mysql@192.168.171.203:3306/test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@192.168.171.203:3306/test'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)
manager = Manager(app)


# 请求钩子
@app.before_first_request
def before_first_request():
    """
    
    :return: 
    """
    print("before first request")


@app.before_request
def before_request():
    """
    
    :return: 
    """
    print("before request")


@app.after_request
def after_request(Response):
    """
    
    :param Response: 
    :return: 
    """
    print("after_request")
    return Response


@app.teardown_request
def teardown_request(e):
    """
    
    :param : 
    :return: 
    """
    print("teardown_request")


# 数据库操作
if __name__ == '__main__':

    # db.drop_all()
    # db.create_all()
    app.run(port=8000, debug="DEBUG")

# 从对象加载
app.config.from_object(Config)

# 从文件加载
# app.config.from_pyfile("config.ini")
# 读取配置文件
# app.config.get()
