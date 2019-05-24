# coding=utf-8
from flask import Blueprint

index_blu = Blueprint("user", __name__)

from info.modules.user import views

print("调用index.init")
