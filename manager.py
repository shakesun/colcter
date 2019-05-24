# coding=utf-8

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# from flask import Flask

from info import db, create_app

app = create_app("development")
# app = Flask(__name__)

manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)
# print("调用manager3")

# 数据库操作
if __name__ == '__main__':

    # print(app)
    # db.create_all()
    # app.run()
    print("调用manager1")

    manager.run()
    # app.run()

