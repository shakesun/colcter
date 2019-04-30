# coding=utf-8
from flask import Blueprint

index_blu = Blueprint("index", __name__)

from .views import views
print("调用index.init")
