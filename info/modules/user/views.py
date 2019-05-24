# coding=utf-8
# from manager import app
from info.modules.user import index_blu
from info.models import User
from flask import request, session, abort
from flask import jsonify
from flask import current_app
from utils.response_code import error_map, RET
from info import redis_store
from datetime import datetime
from info import db
from utils.smscode_sender.sms_sender import CCP
import re
import random
from info import constants


@index_blu.route("/users/logout", methods=["GET"])
def logout():
    """
    退出登录
    :return:
    """
    # pop是移除session中的数据(dict)
    # pop 会有一个返回值，如果要移除的key不存在，就返回None
    session.pop('user_id', None)
    session.pop('mobile', None)
    session.pop('nick_name', None)
    # 要清楚is_admin的值，如果不清除，先登录管理员，会保存到session，再登录普通用户，又能访问管理员页面
    # session.pop('is_admin', None)

    return jsonify(errno=RET.OK, errmsg="退出成功")


@index_blu.route("/users/login", methods=["POST"])
def login():
    """
    登陆接口
    1. 获取参数
    2. 校验参数
        1. 是否存在此用户
        2. 密码是否正确
    3. 保持登陆状态
    :return: 
    """
    param_dict = request.json
    mobile = param_dict.get("mobile")
    password = param_dict.get("password")

    print(mobile)
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if not re.match('1[35678]\\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")

    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    if user is None:
        return jsonify(errno=RET.USERERR, errmsg="用户名错误或不存在")

    # 验证密码是否正确

    session["user_id"] = user.user_id
    session["mobile"] = user.mobile
    session["nick_name"] = user.nick_name

    user.last_login = datetime.now()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)

    return jsonify(errno=RET.OK, errmsg="登录成功")


@index_blu.route('/users/register', methods=["POST"])
def register():
    """
    注册路由
    :return: 
    """
    param_dict = request.json
    mobile = param_dict.get("mobile")
    smscode = param_dict.get("smscode")
    password = param_dict.get("password")
    if not all([mobile, smscode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if not re.match('1[35678]\\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")

    # 验证码校验
    try:
        real_sms_code = redis_store.get("SMS_" + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")

    if not real_sms_code:
        return jsonify(errno=RET.NODATA, errmsg="验证码已过期")
    a = int(real_sms_code)
    b = int(smscode)
    print(a)
    print(b)
    if int(real_sms_code) != int(smscode):
        return jsonify(errno=RET.DATAERR, errmsg="验证码输入错误")

    user = User()
    user.mobile = mobile     # 暂时没有昵称 ，使用手机号代替
    user.nick_name = mobile     # 记录用户最后一次登录时间
    user.last_login = datetime.now()     # 对密码做处理
    # 需求：在设置 password 的时候，去对 password 进行加密，并且将加密结果给 user.password_hash 赋值
    user.password = password

    # 添加到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="数据保存失败")

    # 往 session 中保存数据表示当前已经登录
    session["user_id"] = user.user_id
    session["mobile"] = user.mobile
    session["nick_name"] = user.nick_name

    return jsonify(errno=RET.OK, errmsg="注册成功")


@index_blu.route('/users/smscode', methods=["POST"])
def smscode():
    """
    发送短信验证码接口
    1. 获取手机号
    2. 校验手机号是否格式正确
    3. 查看手机号是否已经注册
    4. 发送手机验证码
    5. 将手机验证码存储在redis中
    :return: 
    """
    param_dict = request.json
    mobile = param_dict.get("mobile")
    print(mobile)
    if not all([mobile]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if not re.match('1[35678]\\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")

    # 校验用户是否已经注册
    try:
        exi_mobile = User.query.filter_by(mobile=mobile).get()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")

    if exi_mobile is not None:
        return jsonify(errno=RET.USERERR, errmsg="该手机号已经注册")

    # 发送手机验证码
    sms_code = random.randint(100000, 999999)
    sms_sender = CCP()
    sms_sender.send_template_sms(mobile, [sms_code, 5], 1)

    # 将验证码存储在redis当中
    try:
        redis_store.set("SMS_"+mobile, sms_code, ex=constants.SMS_CODE_EXPIRE)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    return jsonify(errno=RET.OK, errmsg="发送成功")
