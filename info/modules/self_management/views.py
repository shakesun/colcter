# coding=utf-8

from info.modules.self_management import self_manage_blu
from info.models import Target, Todo_list, Plan, Profession
from flask import request, session, abort
from flask import jsonify, current_app, g, redirect
from info import db
from utils.response_code import RET
from utils.commen import user_login_data


@self_manage_blu.route("/profset", methods=["POST"])
@user_login_data
def set_profession():
    """
    1. 获取参数
    :return: 
    """

    user = g.user

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户未登录")

    user_id = session.get("user_id")
    param_dict = request.json
    profession_name = param_dict["profession_name"]
    profession = Profession()
    profession.prof_name = profession_name
    profession.user_id = user_id

    # 添加到数据库
    try:
        db.session.add(profession)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="数据保存失败")

    prof_dict = profession.to_dict()

    return jsonify(profession_name=prof_dict)


@self_manage_blu.route("/set_major", methods=["POST"])
@user_login_data
def set_prof_major():
    """
    1. 获取参数prof_id, major_or_not 
    2. 判断 major_or_not 的值，并修改
    3. 返回 major_or_not 的值
    :return: 
    """
    user = g.user

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户未登录")

    param_dict = request.json
    prof_id = param_dict["prof_dict"]
    major_or_not = param_dict["major_or_not"]

    profession = Profession.query.filter_by(prof_id=prof_id).first()
    if major_or_not is True:
        profession.major_or_not = False
    elif major_or_not is False:
        profession.major_or_not = True
    else:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        db.session.add(profession)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="数据保存失败")

    # TODO 返回的参数
    return jsonify(major_or_not=major_or_not)


@self_manage_blu.route("/set_tg")
@user_login_data
def set_target():
    """
    
    :return: 
    """
    user = g.user

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户未登录")

    return "set_tg"


@self_manage_blu.route("/set_plan")
@user_login_data
def set_plan():
    """
    
    :return: 
    """
    user = g.user

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户未登录")

    return


@self_manage_blu.route("/set_todo")
@user_login_data
def set_todolist():
    """
    
    :return: 
    """
    user = g.user

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户未登录")

    return


@self_manage_blu.route("/feedback")
@user_login_data
def plan_feedback():
    """
    
    :return: 
    """
    user = g.user

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户未登录")

    return
