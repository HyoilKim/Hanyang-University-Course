from flask import Flask, render_template, request
from db import search_customerInfo, insert_customerInfo, set_type, get_hosp_list, visited_record, visit_hospital
from db import add_favorite_hospital, update_hospInfo_table, update_pharmInfo_table, get_pharm_list
from db import get_favorite_hospital_list, add_reservation, get_institution_name, reservation_list
from db import cancel_reservation, add_description, search_description_record, pharmacy_search_description
from db import set_pharmacy_status, add_pharmacy_description, patient_visited_record, patient_search_description
from db import visit_pharmacy, get_patient_name, glasses_search_description, add_glasses_description, visit_glasses, glasses_list
import json
from pprint import pprint
from datetime import datetime
# from apicall import hosp_list, pharm_list

app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# 로그인 화면
@app.route('/')
def index():            
    return render_template("sign-in.html")       

@app.route('/login', methods=["POST"])
def login():
    return render_template("sign-in.html")

# 로그인 정보가 올바른지 확인
@app.route("/sign-in", methods=["GET", "POST"])                        
def sign_in():           
    email = request.form.get('email')
    tmp = email.split('@')
    local = tmp[0]
    print(tmp)
    domain = tmp[1]
    password = request.form.get('password')
    res = search_customerInfo(local, domain, password)
    print(res)
    if res == []: return "회원정보가 없습니다. 회원가입을 해주세요."
    if res[0][0] == "patient": return render_template("patient-main.html")
    if res[0][0] == "hospital": return render_template("hospital-main.html")
    if res[0][0] == "pharmacy": return render_template("pharmacy-main.html")
    if res[0][0] == "glasses": return render_template("glasses-main.html")
    return "error"
    #  res의 type종류에 따라 다른 화면 송출
    #  type이 없다면 설정
    #  login data가 없다면 alert  

# 회원가입 화면
@app.route('/sign-up')
def sing_up():
    return render_template("sign-up.html")    

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
@app.route('/patient-main', methods=["POST"])
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

@app.route('/pharmacy_list', methods=["POST"])
def pharmacy_list():
    req = request.get_json()
    lat = req["lat"]
    lng = req["lng"]
    res = update_pharmInfo_table(lat, lng)
    if res == -1: return -1;
    list = get_pharm_list()
    return json.dumps(list)

@app.route('/glasses_list', methods=["POST"])
def get_glasses_list():
    return json.dumps(glasses_list())

@app.route('/add_favorite', methods=["POST"])
def add_favorite():
    req = request.get_json()
    name = req['hospital_name']
    local = req['local']
    domain = req['domain']
    add_favorite_hospital(name, local, domain)
    return json.dumps(get_favorite_hospital_list(local, domain))

@app.route('/add_reservation', methods=["POST"])
def add_reservation_info():
    name = request.form.get('patient_name')
    date = request.form.get('date')
    institution = request.form.get('institution_name')
    phone_number = request.form.get('phone_number')
    add_reservation(name, date, institution, phone_number) 
    return render_template("patient-main.html")

# 병원or약국 관리자가 예약 list를 보는 것
@app.route('/reservation_list', methods=["POST"])
def reservation_patient():
    req = request.get_json()
    local = req['local']
    domain = req['domain']
    tmp = get_institution_name(local, domain)
    print(tmp)
    if(tmp == []):
        print("xxxx")
        return tmp
    institution_name = tmp[0][0]
    return json.dumps(reservation_list(institution_name))
    
@app.route('/cancel_reservation', methods=["POST"])
def delete_reservation():
    print("cancel")
    req = request.get_json()
    local = req['local']
    domain = req['domain']
    serial_number = req['serial_number']
    tmp = get_institution_name(local, domain)
    hospital_name = tmp[0][0]
    cancel_reservation(hospital_name, serial_number)
    print("cancel")    
    return json.dumps(reservation_list(hospital_name))   #취소하고 다시 reload

@app.route('/add_hospital_description', methods=["POST"])
def description():
    req = request.get_json()
    hospital_date = req['hospital_date']
    patient_name = req['patient_name']
    serial_number = req['serial_number']
    medicine_name = req['medicine_name']
    amount_per_onetime = req['amount_per_onetime']
    count_per_oneday = req['count_per_oneday']
    how_long_day = req['how_long_day']
    local = req['local']
    domain = req['domain']
    tmp = get_institution_name(local, domain)
    hospital_name = tmp[0][0]
    # 병원이 처방하면 방문기록에 추가
    visit_hospital(patient_name, hospital_name, hospital_date)
    return json.dumps(add_description(hospital_date, patient_name, serial_number, hospital_name, medicine_name
                            , amount_per_onetime, count_per_oneday, how_long_day))

@app.route('/add_glasses_description', methods=["POST"])
def glasses_description():
    req = request.get_json()
    date = req['date']
    recommend_date = req['recommend_date']
    patient_name = req['patient_name']
    r_vision = req['r_vision']
    l_vision = req['l_vision']
    fixed_l_vision = req['fixed_l_vision']
    fixed_r_vision = req['fixed_r_vision']
    local = req['local']
    domain = req['domain']
    tmp = get_institution_name(local, domain)
    hospital_name = tmp[0][0]
    # 병원이 처방하면 방문기록에 추가
    visit_hospital(patient_name, hospital_name, date)
    return json.dumps(add_glasses_description(date, recommend_date, patient_name, hospital_name, l_vision, r_vision
                            , fixed_l_vision, fixed_r_vision))

@app.route('/search_description_record', methods=["POST"])
def search_description():
    req = request.get_json()
    date = req['date']
    patient_name = req['patient_name']
    serial_number = req['serial_number']
    detail = search_description_record(patient_name, serial_number, date)
    return json.dumps(detail)

@app.route('/glasses_search_description', methods=["POST"])
def glasses_search_descrip():
    req = request.get_json()
    local = req['local']
    domain = req['domain']
    tmp = get_institution_name(local, domain)
    glasses_store_name = tmp[0][0]
    date = req['date']
    patient_name = req['patient_name']
    detail = glasses_search_description(patient_name, glasses_store_name, date)
    return json.dumps(detail)

@app.route('/glasses_prescribe', methods=["POST"])
def glasses_store_prescribe():
    patient_name = request.form.get('patient_name')
    date = request.form.get('date')
    glasses_store_name = request.form.get('glasses_name')

    # name = request.form.get('patient_name')
    # req = request.get_json()
    # local = req['local']
    # domain = req['domain']
    # tmp = get_institution_name(local, domain)
    # glasses_store_name = tmp[0][0]
    # serial = req['serial']
    # patient_name = req['patient_name']
    visit_glasses(patient_name, glasses_store_name, date)
    return render_template("glasses-main.html")


@app.route('/patient_search_description', methods=["POST"])
def patient_search_descrip():
    # name = request.form.get('patient_name')
    req = request.get_json()
    local = req['local']
    domain = req['domain']
    tmp = get_institution_name(local, domain)

    name = tmp[0][0]
    print(name)
    detail = patient_search_description(name)
    print(detail)
    return json.dumps(patient_search_description(name))
    # return render_template("personal-description.html", description=patient_search_description(name))

@app.route('/pharmacy_search_description', methods=["POST"])
def pharmacy_search_descrip():
    req = request.get_json()
    local = req['local']
    domain = req['domain']
    date = req['date']
    patient_name = req['patient_name']
    serial_number = req['serial_number']
    tmp = get_institution_name(local, domain)
    pharmacy_name = tmp[0][0]
    
    # 예약목록중에 처방받은 사람만 조회가능(예약리스트, 처방리스트)
    detail = pharmacy_search_description(patient_name, serial_number, date, pharmacy_name)
    return json.dumps(detail)

@app.route('/pharmacy_description', methods=["POST"])
def pharmacy_description():
    return render_template("pharmacy-description.html")

@app.route('/pharmacy_description_finish', methods=["POST"])
def pharmacy_description_finish():
    req = request.get_json()
    local = req['local']
    domain = req['domain']
    id = req['number']
    date = req['date']
    contents = req['description_contents']
    tmp = get_institution_name(local, domain)
    pharmacy_name = tmp[0][0]
    res = add_pharmacy_description(id, date, contents, pharmacy_name)
    if res == -1: return "no"
    # 처방에 성공하면 방문기록에 추가
    tmp = get_patient_name(id)
    patient_name = tmp[0][0]
    visit_pharmacy(patient_name, pharmacy_name, date)
    return "ok"

@app.route('/pharmacy_main', methods=["POST"])
def pharmacy():            
    return render_template("pharmacy-main.html")      

@app.route('/set_pharmacy_status', methods=["POST"])
def set_pharmacy_state():
    req = request.get_json()
    number = req['serial_number']
    set_pharmacy_status(number, "no")
    return "ok"

@app.route('/patient_visited_record', methods=["POST"])
def patient_visiting_record():
    email = request.get_json()
    local = email['local']
    domain = email['domain']
    tmp = get_institution_name(local, domain)
    patient_name = tmp[0][0]
    return json.dumps(patient_visited_record(patient_name))
    
@app.route('/visit_record', methods=["POST"])
def visit_record():
    req = request.get_json()
    local = req['local']
    domain = req['domain']
    tmp = get_institution_name(local, domain)
    institution_name = tmp[0][0]
    return json.dumps(visited_record(institution_name))


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == ("__main__"):
  app.run(debug=True, host='0.0.0.0', port=5000)