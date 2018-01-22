#-*-coding:utf-8-*-
#-*-coding:utf-8-*-
import os
from datetime import timedelta
DEBUG = True
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME='root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'zlktqa_demo'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 24个字符字符串
SECRET_KEY = os.urandom(24)
# session 过期时间
PERMANENT_SESSION_LIFETIME = timedelta(days=7)