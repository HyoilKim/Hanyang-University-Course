# 서버 역할을 하는 code
from flask import Flask, render_template, request
from pypg.db import db_insert, db_search, db_delete, db_update, init_table, create_table
import json
from pprint import pprint

app = Flask(__name__)

@app.route('/')   #127.0.0.1:5090의 기본페이지
def index():
    # table을 생성하고 초기화 하는 코드 -> 한 번 실행 후 주석처리 해야함
    # create_table("phonebook1") 
    # init_table()
    return render_template("index.html")                                #index.html파일 show(코드분리)

@app.route("/search-json", methods=["GET", "POST"])                          #register라는 url에서 두개의 http request가능
def search_json():
    # json to string
    req = request.get_json()
    print(req)
    name = req['name']
    print(name)
    students = json.dumps(db_search(name));   
    print(students)
    return students
    
@app.route("/register-json", methods=["POST"])
def register_json():
     print("JSON: ", request.is_json)
     print(json.dumps(request.get_json()))
     pprint(request.__dict__)
     return "OK"

@app.route("/insert", methods=["GET", "POST"])  
def insert():
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get("number")   
        print(f"{name}의 전화번호: {number}")
        
        # 서버 호출의 마지막에는 view function을 실행해야 함
        if (db_insert(name, number) == 1):
            return render_template("success.html")
        else:
            return render_template("fail.html")

@app.route("/update", methods=["GET", "POST"])  
def update():
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get("number")  
        new_number = request.form.get("new_number")

        if (db_update(name, number, new_number) == 1):
            return render_template("success.html")
        else:
            return render_template("fail.html")

@app.route("/delete", methods=["GET", "POST"])  
def delete():
    if request.method == 'POST':
        name = request.form.get('name')
        number = request.form.get("number")   
        print(f"{name}의 전화번호: {number}")

        if (db_delete(name, number) == 1):
            return render_template("success.html")
        else:
            return render_template("fail.html")

if __name__ == ("__main__"):
  app.run(debug=True, host='0.0.0.0', port=5090)
  # other
  # app.run(debug=True)
