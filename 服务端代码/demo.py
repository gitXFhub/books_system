import pymysql
from flask import Flask, flash, jsonify, make_response, request, redirect, url_for, send_from_directory,Response
from flask_cors import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app,supports_credentials=True,resources='/*')
db = pymysql.connect(host="localhost",user="jfinal",passwd="jfinal01@2021",database="jfinal01")
cur = db.cursor()

def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

def create_user(sname,sno,pwd):
    sql = f"insert into student values('{sno}','{sname}','{pwd}')"
    sel = f"select * from student where sno='{sno}'"
    try:
        cur.execute(sel)
        results = cur.fetchall()
        if len(results) > 0:
            return jsonify({"create":'学号已被别人注册'})
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()
        return jsonify({"create":False})
    return jsonify({"create":True})

def login(sno,pwd):
    sel = f"select * from student where sno='{sno}'"
    try:
        cur.execute(sel)
        results = cur.fetchall()
        for row in results:
            password = row[2]
            if pwd != password:
                return jsonify({"login":False,"msg":'账号或密码错误!'})
    except:
        db.rollback()
        return jsonify({"login":False})
    return jsonify({"login":True})

@app.route('/login/')
def hello_world():  # put application's code here
    if request.method == 'POST':
        print('不能用post!!')
        return '不支持post方法!'
    else:
        try:
            sno = request.values.get('idname')
            pwd = request.values.get('psw')
            return make_response(login(sno,pwd))
        except:
            return make_response(jsonify({"login":False}))


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        print('不能用post!!')
        return '不支持post方法!'
    else:
        try:
            name = request.values.get('name')
            sno = request.values.get('idname')
            pwd = request.values.get('psw')
            response = make_response(create_user(name,sno,pwd))
            return response
        except:
            return jsonify({"create":False})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.after_request(after_request)
