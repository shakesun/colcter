# coding=utf-8
from flask import Blueprint

self_manage_blu = Blueprint("self_management", __name__, url_prefix="/manager")

from info.modules.self_management import views
