# coding=utf-8

import functools
from flask import g, current_app
from flask import session
from info.models import User


def user_login_data(f):
    # functools.wraps保证被装饰的函数__name__不变
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        use_id = session.get("user_id", None)
        user = None
        if use_id:
            try:
                user = User.query.get(use_id)
            except Exception as e:
                current_app.logger.error(e)
        g.user = user
        return f(*args, **kwargs)
    return wrapper
