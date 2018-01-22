#-*-coding:utf-8-*-
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from zlkt import app
from exts import db
from models import User, Question, Answer, File
manager = Manager(app)
# 使用migrate绑定app和db
migrate = Migrate(app, db)
# 添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)

# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade
if __name__ == '__main__':
    manager.run()