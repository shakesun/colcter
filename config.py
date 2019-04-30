# coding=utf-8
import redis
import logging
print("调用config")


class Config(object):
    """
    配置信息
    """
    SECRET_KEY = "EjpNVSNQTyGi1VvWECj9TvC/+kq3oujee2kTfQUs8yCM6xX9Yjq52v54g+HVoknA"

    LOG_LEVEL = logging.DEBUG
    DEBUG = True

    # mysql配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@192.168.171.203:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # redis配置信息
    REDIS_HOST = '192.168.171.203'
    REDIS_POST = 6379
    #
    # flask_Session配置信息
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_POST)
    PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
    """
    开发环境e
    """
    DEBUG = True


class ProductionConfig(Config):
    """生产环境"""
    pass


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
