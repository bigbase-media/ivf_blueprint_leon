# -*- coding: utf-8 -*-

import os, json
from flask import Flask, jsonify;
from flask import request;
from flask_script import Manager;
import sys

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
    hi_str = '<h1>Hi, proj-hypnos-v2 user\n'
    return hi_str


@app.route('/task', methods=['POST'])
def task_func():
    inputs = request.data
    print(inputs)

    # 调用框架你自定义的函数
    ret = dict()
    ret['code'] = 0
    ret['message'] = "ok"
    ret['data'] = dict()

    resp = jsonify(ret)
    resp.status_code = 200
    return resp

if __name__=='__main__':
    print('Hi, this is IVF_blueprint_leon program')
    manager.run()
