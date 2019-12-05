from flask import Flask, render_template, request
from db import search_customerInfo, insert_customerInfo, set_type, get_hosp_list, visited_record, update_hospInfo_table
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
    if res[0][0] == "patient": return render_template("patient-main.html")
    if res[0][0] == "hospital": return "hosp"
    if res[0][0] == "pharmacy" : return "store"  
    #  res의 type종류에 따라 다른 화면 송출
    #  type이 없다면 설정
    #  login data가 없다면 alert  

# 회원가입 화면
@app.route('/sign-up')
def sing_up():
    return render_template("sign-up.html")    
    
# type이 정해지지 않은 기존 고객들 type선택
@app.route('/after-set-type', methods=["GET", "POST"])
def after_set_type():
    console.log("@")
    email = request.form.get('email')
    tmp = email.split('@')
    local = tmp[0]
    tmp = tmp[1].split('\n')
    domain = tmp[0]
    type = request.form.get('type')
    if type=="patient" or type=="hospital" or type=="store":
        set_type(local, domain, type)
    else: 
        return "잘못된 타입이 들어옴"
    console.log("@")
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

#환자 메인 페이지로 이동
@app.route('/patient-main')
def patient():            
    return render_template("patient-main.html")   

@app.route('/hospital_list', methods=["POST"])
def hospital_list():
    # lat lng 필요
    req = request.get_json()
    lat = req["lat"]
    lng = req["lng"]
    res = update_hospInfo_table(lat, lng)
    if res == -1: return -1;
    list = get_hosp_list()
    return json.dumps(list)

@app.route('/patient-privacy-info', methods=["POST"])
def patient_privacy_info():
    email = request.get_json()
    local = email['local']
    domain = email['domain']
    return json.dumps(visited_record(local, domain))

@app.route('/add_favorite', methods=["POST"])
def add_favorite():
    req = request.get_json()
    name = req['hospital_name']
    local = req['local']
    domain = req['domain']
    return add_favorite_hospital(name, local, domain)


@app.route('/reservation')
def update_hospital():
    print("update_hopital")
    return "OK"    

@app.route('/description')
def update_pharmacy():
    print("update_pharmacy")
    return "OK"


            
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == ("__main__"):
  app.run(debug=True, host='0.0.0.0', port=5000)