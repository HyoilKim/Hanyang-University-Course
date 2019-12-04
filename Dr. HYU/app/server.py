from flask import Flask, render_template, request
from pypg import search_customerInfo, insert_customerInfo, set_type
import json
from pprint import pprint
# from apicall import hosp_list, pharm_list

app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# 로그인 화면
@app.route('/')
def index():            
    return render_template("sign-in.html")       

# 로그인 정보가 올바른지 확인
@app.route("/sign-in", methods=["GET", "POST"])                        
def sign_in():           
    email = request.form.get('email')
    tmp = email.split('@')
    local = tmp[0]
    tmp = tmp[1].split('\n')
    domain = tmp[0]
    password = request.form.get('password')
    res = search_customerInfo(local, domain, password)
    print(res)
    if res == []: return "회원정보가 없습니다. 회원가입을 해주세요."
    if res[0][0] == "no Type": return render_template("set-type.html")
    if res[0][0] == "1": return render_template("patient.html")
    if res[0][0] == "2": return "hosp"
    if res[0][0] == "3" : return "store"
    
    #  res의 type종류에 따라 다른 화면 송출
    #  type이 없다면 설정
    #  login data가 없다면 alert

# 회원가입 화면
@app.route('/sign-up')
def sing_up():
    return render_template("sign-up.html")    

@app.route('/ajax')
def ajax():
    return "OK"
    
# type이 정해지지 않은 기존 고객들 type선택
@app.route('/after-set-type', methods=["GET", "POST"])
def after_set_type():
    email = request.form.get('email')
    tmp = email.split('@')
    local = tmp[0]
    tmp = tmp[1].split('\n')
    domain = tmp[0]
    type = request.form.get('type')
    if type=="1": type="patient"
    elif type=="2": type="hosp"
    elif type=="3": type="store"
    else: return "잘못된 타입이 들어옴"
    set_type(local, domain, type)
    return render_template("sign-in.html")

# 입력받은 정보를 고객목록에 추가(회원가입)
@app.route('/add-customer', methods=["GET", "POST"])
def add_customer():
    req = request.get_json()
    email = req['email']
    tmp = email.split('@')
    local = tmp[0]
    tmp = tmp[1].split('\n')
    domain = tmp[0]
    password = req['password']
    name = req['name']
    phone_number = req['phone_number']
    type = req['type']
    tmp = insert_customerInfo(name, phone_number, local, domain, password, type)
    if tmp == "회원정보존재":
        return "가입실패"
    else:
        return "가입성공"

@app.route('/patient')
def patient():            
    return render_template("index.html")   

@app.route('/hospital_list')
def hospital_list:


#api콜 수행으로 병원, 상점, 위치 다시받아와서 ajax에 return
@app.route('/update_hospital')
def update_hospital():
    print("update_hopital")
    return "OK"    

@app.route('/update_pharmacy')
def update_pharmacy():
    print("update_pharmacy")
    return "OK"

@app.route('/update_optician')
def update_optician():
    print("update_optician")
    return "OK"





@app.route('/hosp')
def hosp():
    return ""

@app.route('/store')
def store():
    return "OK"

@app.route("/search-json", methods=["GET", "POST"])                          
def search_json():
    # json to string
    req = request.get_json()
    print(req)
    name = req['name']
    print(name)
    students = json.dumps(db_search(name));   
    print(students)
    return students

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
            
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == ("__main__"):
  app.run(debug=True, host='0.0.0.0', port=5000)