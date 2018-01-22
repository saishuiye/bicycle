#encoding: utf-8
from flask import Flask,render_template, request, redirect, url_for, session, g
import config
from models import User, Question, Answer
from exts import db
import csv, operator,os
from sqlalchemy import or_
from decorators import login_required
from werkzeug.utils import secure_filename
from gevent import monkey
monkey.patch_all()
from gevent import pywsgi
import subprocess
import time

app = Flask(__name__)
app.config.from_object(config)
# 不写这句注册会报错
db.init_app(app)

@app.route('/line/')
def line():
    return render_template('line.html')

@app.route('/map1/')
def map1():
    return render_template('map1.html')

# @app.route('/')
# def index():
#     context = {
#         'questions': Question.query.order_by('-create_time').all()
#     }
#     return render_template('index.html',**context)

import threading
import multiprocessing
@app.route('/', methods=['POST', 'GET'])
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all(),
        'is_success':False
    }
    print("asyn has a request!")
    # time.sleep(10)
    # lease_frequency()
    # basepath = os.path.dirname(__file__)  # 当前文件所在路径
    # print basepath
    # os.system('cd'+basepath)
    # os.system('python a.py')
    p = multiprocessing.Process(target=lease_frequency)
    p.start()
    # os.system('python ./a.py')
    # processor = "a.py"
    # INTERPRETER = "/usr/bin/python"
    # pargs = [INTERPRETER, processor]
    # pargs.extend(["--input=inputMd5s"])
    # subprocess.Popen(pargs)

    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static\upload',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        context['is_success'] = True
        # return redirect(url_for('uploads'))

    return render_template('index.html', **context)


@app.route('/lease_frequency/')
def lease_frequency():
    print 11111111111111111111111111111111111
    frequency = {}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'static/uploads/train.csv'))as csvfile:
        reader = [each for each in csv.DictReader(csvfile)]
        base = len(reader)
        for row in reader:
            time = int(row['OVERTIME'])
            if time not in frequency:
                frequency[time] = 1
            else:
                frequency[time] += 1

        for each in frequency:
            frequency[each] = frequency[each] / float(base)
        minutes = frequency.keys()
        fre = frequency.values()
        result = {'min':minutes,
                  'fre':fre
                  }
        print '======================================'
        print result
    return 'finished!!'
    # return render_template('lease_frequency.html', **result)


@app.route('/route/')
def route():
    return render_template('route.html')


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号或密码错误！'


@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist2.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '改手机号已被注册，请更换手机号码'
        else:
            if password1 != password2:
                return '两次密码不相同'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                # 注册成功，页面跳转到登录页面
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # session.pop('user_id')
    del session['user_id']
    # session.clear()
    return redirect(url_for('login'))


@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

# 执行顺序
# before_request -> 视图函数-> context_processor
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id== user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user':g.user}
    # user_id = session.get('user_id')
    # if user_id:
    #     user = User.query.filter(User.id == user_id).first()
    #     if user:
    #         return {'user':user}
    return {}

@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html',question=question_model)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    # user_id = session['user_id']
    # user = User.query.filter(User.id== user_id).first()
    answer.author = g.user
    answer.question = Question.query.filter(Question.id == question_id).first()
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/search/')
def search():
    q = request.args.get('q')
    # 或条件，title或者content中包含
    questions = Question.query.filter(or_(Question.title.contains(q),
            Question.content.contains(q))).order_by('-create_time')
    return render_template('index.html', questions=questions)




if __name__ == '__main__':
    app.run('127.0.0.1', 5001)
    # server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    # server.serve_forever()