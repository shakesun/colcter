# coding=utf-8

from info.modules.self_management import self_manage_blu
from info.models import Target, Todo_list, Plan, Profession
from flask import request, session, abort
from flask import jsonify


@self_manage_blu.route("/profset")
def set_profession():
    """
    
    :return: 
    """
    return "profset"


@self_manage_blu.route("/set_major")
def set_prof_major():
    """
    
    :return: 
    """
    return "set_major"


@self_manage_blu.route("/set_tg")
def set_target():
    """
    
    :return: 
    """
    return "set_tg"


@self_manage_blu.route("/set_plan")
def set_plan():
    """
    
    :return: 
    """
    return


@self_manage_blu.route("/set_todo")
def set_todolist():
    """
    
    :return: 
    """
    return


@self_manage_blu.route("/feedback")
def plan_feedback():
    """
    
    :return: 
    """
    return
