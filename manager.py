# coding=utf-8

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from info import db, create_app


app = create_app("development")
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)
print("调用manager")

# 数据库操作
if __name__ == '__main__':

    # db.drop_all()
    # db.create_all()
    # app.run()
    manager.run()

