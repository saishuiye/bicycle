#-*-coding:utf-8-*-
from gevent import monkey

monkey.patch_all()
from flask import Flask
from gevent import pywsgi
import time
app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World'

@app.route('/asyn/', methods=['GET'])
def test_asyn_one():
    print("asyn has a request!")
    time.sleep(8)
    print ("111111111111111111")
    return 'hello asyn'

server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
server.serve_forever()
#
# # 文件头部
# from gevent import monkey
# from gevent.pywsgi import WSGIServer
# from flask import Flask,render_template, request, redirect, url_for, session, g
# import time
#
# # gevent的猴子魔法
# monkey.patch_all()
#
# app = Flask(__name__)
#
# app.config.update(DEBUG=True)
#
# @app.route('/asyn/', methods=['GET'])
# def test_asyn_one():
#     print("asyn has a request!")
#     time.sleep(10)
#     return 'hello asyn'
#
#
# @app.route('/test/', methods=['GET'])
# def test():
#     return 'hello test'
#
#
# if __name__ == '__main__':
#     # app.run()
#     # app.run()
#     http_server = WSGIServer(('', 5000), app)
#     http_server.serve_forever()