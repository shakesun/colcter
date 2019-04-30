# coding=utf-8
import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import config
from info.modules.index.views import RegexConverter

db = SQLAlchemy()
redis_store = None

print("调用info.__init__")


def create_app(config_name):
    """
    
    :return: 
    """
    setup_log(config_name)
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # app.secret_key = "tree"
    # app.url_map.converters["re"] = RegexConverter
    db.init_app(app)
    global redis_store
    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_POST)
    CSRFProtect(app)
    Session(app)
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    return app


def setup_log(config_name):
    """
    配置日志
    :return: 
    """

    logging.basicConfig(level=config[config_name].LOG_LEVEL)
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)
