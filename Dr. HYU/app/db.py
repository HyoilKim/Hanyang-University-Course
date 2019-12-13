import psycopg2 as pg
import psycopg2.extras
import json
import requests
from pprint import pprint
import random
# localhost == 127.0.0.1\
pg_local = {
    'host': "localhost", # localhost
    'user': "postgres",  # dbuser
    'dbname': "postgres",  # dbapp
    'password': "gydlf1894*"     
}
db_connector = pg_local
connect_string = "host={host} user={user} dbname={dbname} password={password}".format(
    **db_connector)   

def search_customerInfo(local, domain, password):   
    sql = f'''SELECT type 
              FROM customers_Info 
              WHERE local=\'{local}\' and domain=\'{domain}\' and password=\'{password}\'; 
           '''
    try:
        conn = pg.connect(connect_string) 
        cur = conn.cursor()      
        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()
        conn.close()
        print(result)
        if result == []: return []
        else: return result
    except Exception as e:
        print(e)
        return []    

def set_type(local, domain, type):
    print(type)
    sql = f'''UPDATE customers_Info
              SET type = \'{type}\'
              WHERE local = \'{local}\' and domain = \'{domain}\'
    '''
    try:
        conn = pg.connect(connect_string) 
        cur = conn.cursor() 
        print(sql)    
        cur.execute(sql)
        conn.commit()
        conn.close()
        return 1
    except Exception as e:
        print(e)
        return []    

def insert_customerInfo(name, phone_number, local, domain, password, type):
    sql = f'''INSERT INTO customers_Info(name, phone_number, local, domain, password, type)
                      VALUES (\'{name}\', \'{phone_number}\', \'{local}\'
                                    , \'{domain}\', \'{password}\', \'{type}\');
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        tmp = search_customerInfo(local, domain, password)
        print(tmp)
        if tmp == []: 
            cur.execute(sql)
            print(sql)
        else :
            tmp = "회원정보존재"
        conn.commit()
        conn.close()
        return tmp
    except pg.OperationalError as e:
        print(e)
        return -1

# 병원 정보 Table
def hosp_list_api(lat, lng):
    lat = round(lat, 7)
    lng = round(lng, 7)
    url = "http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList"
    default_key = "3wlHL6g1M3i2oO2cnR44opHmafh54ifadIuEPG/oNu09j7iaYXKYs87dgFRZDsxfSWwzzJoVgqRhKyLHUIl96A=="
    params = {
      'pageNo': 1,  
      'numOfRows': 20,              # 가져오는 데이터 개수
      'clCd': 11,                   # 옵션(종합병원)
      'ServiceKey': default_key,    # 발급키
      'xPos': lng, #127.0331892,    # 파라미터로 받아오거나 한양대 위도,경도로 설정
      'yPos': lat, #37.5585146,
      'radius': 5000,               # 위도,경도 중심으로 ?m 까지
      '_type': 'json'               
      
    }
    r = requests.get(url, params=params)    # url에 parm정보추가
    return r.json()          

# api로 불러온 자료 table에 저장
def update_hospInfo_table(lng, lat):
    url = "http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList"
    default_key = "3wlHL6g1M3i2oO2cnR44opHmafh54ifadIuEPG/oNu09j7iaYXKYs87dgFRZDsxfSWwzzJoVgqRhKyLHUIl96A=="
    params = {
      'pageNo': 1,  
      'numOfRows': 20,              # 가져오는 데이터 개수
      'clCd': 11,                   # 옵션(종합병원)
      'ServiceKey': default_key,    # 발급키
      'xPos': lng, #127.0331892,    # 파라미터로 받아오거나 한양대 위도,경도로 설정
      'yPos': lat, #37.5585146,
      'radius': 5000,               # 위도,경도 중심으로 ?m 까지
      '_type': 'json'               
      
    }
    pprint(params)
    r = requests.get(url, params=params)    # url에 parm정보추가
    json = r.json()
    pprint(json)
    print(json['response']['body']['items'])
    if json['response']['body']['items'] == '': 
        print("지도에 병원x")
        return -1
    hosp = json['response']['body']['items']['item']
    
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()  
        removeAll = f'''DELETE FROM hosp_Info '''
        cur.execute(removeAll)
        print(removeAll)     
        for data in hosp: 
            # print(data)
            name = data['yadmNm']
            addr = data['addr']
            lng = data['XPos']
            lat = data['YPos']
            weekday_open = 8
            weekday_close = 19
            weekend_open = 13
            weekend_close = 17
            distance = data['distance']
            doctor_cnt = data['sdrCnt']
            diagnosis_kinds = "종합과목 진료(한방, 치과제외)"
            sql = f'''INSERT INTO hosp_Info(name, addr, lat, lng, distance, weekday_open, weekday_close, 
                                                weekend_open, weekend_close, doctor_cnt, diagnosis_kinds)
                        VALUES (\'{name}\', \'{addr}\', \'{lat}\', \'{lng}\', \'{distance}\'
                                    , \'{weekday_open}\', \'{weekday_close}\', \'{weekend_open}\'
                                        , \'{weekend_close}\', \'{doctor_cnt}\', \'{diagnosis_kinds}\');
            '''
            print(sql)
            cur.execute(sql)
        conn.commit()
        conn.close()
        # print(sql)
    except pg.OperationalError as e:
        print(e)
        return -1
    return 1;

def get_hosp_list():
    sql = f'''SELECT *
              FROM hosp_Info
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)
        print(sql)
        result = cur.fetchall() 
        pprint(result)
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        print(e)
        return -1

def glasses_list():
    sql = f'''SELECT *
              FROM glasses_store
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)
        print(sql)
        result = cur.fetchall() 
        pprint(result)
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        print(e)
        return -1
      
def get_institution_name(local, domain):
    print(local)
    print(domain)
    sql = f'''SELECT name
              FROM customers_Info
              WHERE local=\'{local}\' and domain=\'{domain}\' 
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)
        print(sql)
        result = cur.fetchall() 
        print(result)
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        print(e)
        return -1    

# api로 부터 약국 불러오기
def pharm_list_api(lat, lng):    
    url = "http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList"
    default_key = "3wlHL6g1M3i2oO2cnR44opHmafh54ifadIuEPG/oNu09j7iaYXKYs87dgFRZDsxfSWwzzJoVgqRhKyLHUIl96A=="
    params = {
        'pageNo': 1,
        'numOfRows': 10,
        'ServiceKey': default_key,
        'xPos': lng, #127.0331892,
        'yPos': lat, #37.5585146,
        'radius': 5000,  
        '_type': 'json'
    }
    r = requests.get(url, params=params)
    return r.json()

# 약국 테이블에 api자료로 업데이트
def update_pharmInfo_table(lng, lat):
    url = "http://apis.data.go.kr/B551182/pharmacyInfoService/getParmacyBasisList"
    default_key = "3wlHL6g1M3i2oO2cnR44opHmafh54ifadIuEPG/oNu09j7iaYXKYs87dgFRZDsxfSWwzzJoVgqRhKyLHUIl96A=="
    params = {
        'pageNo': 1,
        'numOfRows': 10,
        'ServiceKey': default_key,
        'xPos': lng, #127.0331892,
        'yPos': lat, #37.5585146,
        'radius': 5000,  
        '_type': 'json'
    }
    pprint(params)
    r = requests.get(url, params=params)    # url에 parm정보추가
    json = r.json()
    pprint(json)
    print(json['response']['body']['items'])
    if json['response']['body']['items'] == '': 
        print("지도에 약국x")
        return -1
    pharm = json['response']['body']['items']['item']
    
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()  
        removeAll = f'''DELETE FROM pharm_Info '''
        print(removeAll)  
        cur.execute(removeAll)   
        for data in pharm: 
            # print(data)
            name = data['yadmNm']
            addr = data['addr']
            lng = data['XPos']
            lat = data['YPos']
            weekday_open = 8
            weekday_close = 19
            weekend_open = 13
            weekend_close = 17
            distance = data['distance']
            
            tmp = f'''SELECT pharmacy_status FROM prescription_list WHERE pharmacy_name=\'{name}\' '''
            cur.execute(tmp)
            status = cur.fetchall()
            print(status)
            if status != []:
                if status[0][0] == "ok":
                    status = "ok"
                elif status[0][0] =="no":
                    status = "no"
            else:
                status = "unknown"
            print(status)
            # prescribe_possible = "ok" # ok, no, unknown
            sql = f'''INSERT INTO pharm_Info(name, addr, lat, lng, distance, weekday_open, weekday_close, 
                                                weekend_open, weekend_close, prescribe_possible)
                        VALUES (\'{name}\', \'{addr}\', \'{lat}\', \'{lng}\', \'{distance}\'
                                    , \'{weekday_open}\', \'{weekday_close}\', \'{weekend_open}\'
                                        , \'{weekend_close}\', \'{status}\');
            '''
            print(sql)
            cur.execute(sql)
        conn.commit()
        conn.close()
        # print(sql)
    except pg.OperationalError as e:
        print(e)
        return -1
    return 1;

# db의 약국정보들 불러오기
def get_pharm_list():
    sql = f'''SELECT *
              FROM pharm_Info
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)
        print(sql)
        result = cur.fetchall() 
        pprint(result)
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        print(e)
        return -1

# db에 약국정보가 있는지 확인하기 위해 하나만 검색 
def get_pharm(name):
    sql = f'''SELECT name
              FROM pharm_Info
              WHERE name=\'{name}\'
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)
        print(sql)
        result = cur.fetchall() 
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        print(e)
        return -1    

def visited_record(institution_name):
    sql = f'''SELECT patient_name, date
              FROM visited_record
              WHERE institution_name=\'{institution_name}\'
              ORDER BY date DESC
    '''
    sql1 = f'''SELECT * FROM visited_record'''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)
        print(sql)
        result = cur.fetchall()
        print(result)

        cur.execute(sql1)
        print(cur.fetchall())
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        return -1

def patient_visited_record(patient_name):
    sql = f'''SELECT institution_name, date
              FROM visited_record
              WHERE patient_name=\'{patient_name}\'
              ORDER BY date DESC
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)
        print(sql)
        result = cur.fetchall()
        print(result)
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        return -1

def visit_hospital(patient_name, hospital_name, date):
    sql = f'''INSERT INTO visited_record(patient_name, institution_name, date)
                      VALUES (\'{patient_name}\', \'{hospital_name}\', \'{date}\');
                      
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        print(sql)
        conn.commit()
        conn.close()
        return 1
    except pg.OperationalError as e:
        print(e)
        return -1

def visit_pharmacy(patient_name, pharmacy_name, date):
    sql = f'''INSERT INTO visited_record(patient_name, institution_name, date)
                      VALUES (\'{patient_name}\', \'{pharmacy_name}\', \'{date}\');
                      
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        print(sql)
        conn.commit()
        conn.close()
        return 1
    except pg.OperationalError as e:
        print(e)
        return -1

def visit_glasses(patient_name, glasses_name, date):
    sql = f'''INSERT INTO visited_record(patient_name, institution_name, date)
              VALUES (\'{patient_name}\', \'{glasses_name}\', \'{date}\');     
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        if cur.fetchall == []: return -1
        cur.execute(sql)
        print(sql)        
        conn.commit()
        conn.close()
        return 1
    except pg.OperationalError as e:
        print(e)
        return -1

def get_patient_name(id):
    sql = f'''SELECT patient_name
              FROM visited_record
              WHERE id=\'{id}\'
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()
        cur.execute(sql)
        print(sql)
        result = cur.fetchall()
        print(result)
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        return -1


def add_hosp(lat, lng):
    json = hosp_list_api(lat, lng)
    hosp = json['response']['body']['items']['item']
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor()         
        for data in hosp: 
            # print(data)
            name = data['yadmNm']
            addr = data['addr']
            lng = data['XPos']
            lat = data['YPos']
            weekday_open = 8
            weekday_close = 19
            weekend_open = 13
            weekend_close = 17
            distance = data['distance']
            doctor_cnt = data['sdrCnt']
            diagnosis_kinds = "종합과목 진료(한방, 치과제외)"
            if get_hosp(name) == []:
                sql = f'''INSERT INTO hosp_Info(name, addr, lat, lng, distance, weekday_open, weekday_close, 
                                                    weekend_open, weekend_close, doctor_cnt, diagnosis_kinds)
                            VALUES (\'{name}\', \'{addr}\', \'{lat}\', \'{lng}\', \'{distance}\'
                                        , \'{weekday_open}\', \'{weekday_close}\', \'{weekend_open}\'
                                            , \'{weekend_close}\', \'{doctor_cnt}\', \'{diagnosis_kinds}\');
                '''
                print(sql)
                cur.execute(sql)
            else:
                print("이미 존재하는 병원")
        conn.commit()
        conn.close()
        # print(sql)
    except pg.OperationalError as e:
        print(e)
        return -1
    return 1;    
        
def add_favorite_hospital(hospital_name, local, domain):
    sql = f'''INSERT INTO favorite_hospital(hospital_name, local, domain)
                      VALUES (\'{hospital_name}\', \'{local}\', \'{domain}\');
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        print(sql)
        conn.commit()
        conn.close()
        return 1
    except pg.OperationalError as e:
        print(e)
        return -1

def get_favorite_hospital_list(local, domain):
    sql = f'''SELECT hospital_name
              FROM favorite_hospital
              WHERE local=\'{local}\' and domain=\'{domain}\'
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        result = cur.fetchall()
        print(sql)
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        print(e)
        return -1

def add_reservation(name, date, institution_name, phone_number):
    print("add reserve")
    sql = f'''INSERT INTO reservation_list(name, date, institution_name, phone_number)
              VALUES (\'{name}\', \'{date}\', \'{institution_name}\', \'{phone_number}\');
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        print(sql)
        conn.commit()
        conn.close()
        return 1
    except pg.OperationalError as e:
        print(e)
        return -1

def reservation_list(institution_name):
    sql = f'''SELECT id, name, phone_number, date
              FROM reservation_list
              WHERE institution_name=\'{institution_name}\'
              ORDER BY date ASC
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        result = cur.fetchall()
        print(sql)
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        print(e)
        return -1

def cancel_reservation(institution_name, id):
    sql = f'''DELETE
              FROM reservation_list
              WHERE id = \'{id}\'
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        print(sql)
        conn.commit()
        conn.close()
        return 
    except pg.OperationalError as e:
        print(e)
        return -1

# 발급 년월일 번호
# 환자 이름
# 병원 이름
# 처방의약품의 명칭, 1회투약량, 1일 투여횟수, 총투약일수
# 조제 연월일
# 병원 이름
def add_description(hospital_date, patient_name, serial_number, hospital_name, medicine_name
                            , amount_per_onetime, count_per_oneday, how_long_day):
    sql = f'''INSERT INTO prescription_list(hospital_date, patient_name, id, hospital_name, medicine_name
                , amount_per_onetime, count_per_oneday, how_long_day)
              VALUES (\'{hospital_date}\', \'{patient_name}\', \'{serial_number}\', 
                            \'{hospital_name}\', \'{medicine_name}\', \'{amount_per_onetime}\'
                                , \'{count_per_oneday}\', \'{how_long_day}\');
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        print(sql)
        conn.commit()
        conn.close()
        return 1
    except pg.OperationalError as e:
        print(e)
        return -1

def add_glasses_description(date, recommend_date, patient_name, name, l_vision, r_vision
                            , fixed_l_vision, fixed_r_vision):
    sql = f'''INSERT INTO glasses_description(hospital_date, recommend_date, patient_name, hospital_name, l_vision
                , r_vision, fixed_l_vision, fixed_r_vision)
              VALUES (\'{date}\', \'{recommend_date}\', \'{patient_name}\', 
                            \'{name}\', \'{l_vision}\', \'{r_vision}\'
                                , \'{fixed_l_vision}\', \'{fixed_r_vision}\');
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        print(sql)
        conn.commit()
        conn.close()
        return 1
    except pg.OperationalError as e:
        print(e)
        return -1

# 처방옵션
def search_description_record(patient_name, serial_number, date):
    sql = f'''SELECT id, hospital_date, patient_name, hospital_name, medicine_name, amount_per_onetime, count_per_oneday, how_long_day
                        ,pharmacy_name, pharmacy_date, pharmacy_opinion
              FROM prescription_list
              WHERE patient_name=\'{patient_name}\' or id=\'{serial_number}\'
                    or hospital_date LIKE \'{date}%\'
    '''
    tmp = f'''SELECT * FROM prescription_list'''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        result = cur.fetchall()
        # cur.execute(tmp)
        # pprint(cur.fetchall())
        print(sql)
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        print(e)
        return -1

# 예약한 환자들 중 처방을 받은 환자 조회
def glasses_search_description(patient_name, glasses_name, date):
    sql = f'''SELECT id, hospital_date, recommend_date, patient_name, hospital_name, l_vision
                , r_vision, fixed_l_vision, fixed_r_vision
              FROM glasses_description
              WHERE hospital_date LIKE \'{date}%\' and 
                            patient_name IN (SELECT name
                            FROM reservation_list
                            WHERE institution_name=\'{glasses_name}\')
    '''
    tmp = f'''SELECT * FROM prescription_list'''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        result = cur.fetchall()
        # cur.execute(tmp)
        # pprint(cur.fetchall())
        print(sql)
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        print(e)
        return -1

def patient_search_description(patient_name):
    sql = f'''SELECT id, pharmacy_name, pharmacy_date, pharmacy_opinion
              FROM prescription_list
              WHERE patient_name=\'{patient_name}\'
    '''
    tmp = f'''SELECT * FROM prescription_list'''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        result = cur.fetchall()
        print(sql)

        cur.execute(tmp)
        print(cur.fetchall())
        conn.commit()
        conn.close()
        print(result)
        return result
    except pg.OperationalError as e:
        print(e)
        return -1

def pharmacy_search_description(patient_name, serial_number, date, pharmacy_name):
    # 예약한 사람들 중 처방을 받은 사람들
    sql = f'''SELECT id, hospital_date, patient_name, hospital_name, medicine_name, amount_per_onetime, count_per_oneday, how_long_day
                        ,pharmacy_name, pharmacy_date, pharmacy_opinion
              FROM prescription_list
              WHERE hospital_date LIKE \'{date}%\' and id=\'{serial_number}\'
                    and patient_name IN (SELECT name
                            FROM reservation_list
                            WHERE institution_name=\'{pharmacy_name}\')
    '''
    sql1 = f'''SELECT * FROM reservation_list WHERE institution_name=\'{pharmacy_name}\' '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        print(sql)
        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()
        conn.close()
        return result
    except pg.OperationalError as e:
        print(e)
        return -1

# 방문 기록 추가
# def add_visited_record(patient_name, hospital_name, date):
#     sql = f'''INSERT INTO visited_record(patient_name, hospital_name, date)
#                       VALUES (\'{patient_name}\', {hospital_name}\', \'{date}\');
#     '''
#     try:
#         conn = pg.connect(connect_string)
#         cur = conn.cursor() 
#         cur.execute(sql)
#         print(sql)
#         conn.commit()
#         conn.close()
#         return 1
#     except pg.OperationalError as e:
#         print(e)
#         return -1

def add_pharmacy_description(id, pharmacy_date, description_contents, pharmacy_name):
    sql = f'''UPDATE prescription_list 
              SET pharmacy_date= \'{pharmacy_date}\'
              WHERE id=\'{id}\'
    '''
    sql1 = f'''UPDATE prescription_list 
              SET pharmacy_opinion= \'{description_contents}\'
              WHERE id=\'{id}\'
    '''
    sql2 = f'''UPDATE prescription_list 
              SET pharmacy_name= \'{pharmacy_name}\'
              WHERE id=\'{id}\'
    '''
    sql3 = f'''UPDATE prescription_list 
              SET pharmacy_status = \'{"ok"}\'
              WHERE id=\'{id}\'
    '''
    sql4 = f'''SELECT * 
               FROM prescription_list
               WHERE id=\'{id}\'
    '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql4)
        if cur.fetchall == []: return -1
        cur.execute(sql)
        print(sql)
        cur.execute(sql1)
        cur.execute(sql2)
        cur.execute(sql3)
        print(sql1)
        conn.commit()
        conn.close()
        return 1
    except pg.OperationalError as e:
        print(e)
        return -1

def set_pharmacy_status(id, status):
    sql = f'''UPDATE prescription_list
              SET pharmacy_status = \'{status}\'
              WHERE id=\'{id}\'
    '''
    sql1 = f'''SELECT * FROM prescription_list '''
    try:
        conn = pg.connect(connect_string) 
        cur = conn.cursor() 
        print(sql)    
        cur.execute(sql)

        cur.execute(sql1)
        print(cur.fetchall())
        conn.commit()
        conn.close()
        return 1
    except Exception as e:
        print(e)
        return []  

if __name__ == ("__main__"):
    lng = 127.0331892    # 파라미터로 받아오거나 한양대 위도,경도로 설정
    lat = 37.5585146
    pprint(hosp_list_api(lat, lng))
    # pprint(get_hosp_list())