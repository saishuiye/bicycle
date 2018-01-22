#-*-coding:utf-8-*-
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(26),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)


    def __init__(self,*args,**kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = generate_password_hash(kwargs.get('password'))

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    uuidname = db.Column(db.String(100),nullable=False)
    realname = db.Column(db.String(40),nullable=False)
    savepath = db.Column(db.String(100),nullable=False)
    uploadtime = db.Column(db.DateTime,default=datetime.now)
    description = db.Column(db.String(255))


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User',backref=db.backref('questions'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question = db.relationship('Question',backref=db.backref('answers',order_by=id.desc()))
    author = db.relationship('User',backref=db.backref('answers'))