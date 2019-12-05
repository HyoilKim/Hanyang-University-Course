import psycopg2 as pg
import psycopg2.extras
import json
import requests
# from apicall import hosp_list, test1
from pprint import pprint
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

# - 추가 되는 정보들 -
# <병원 예약자 명단 Table>
# id ,이름, 전화번호, 시각) 

# <약국 예약자 명단 Table>
# id, 이름, 전화번호, 시각)

# <환자 처방기록 Table>
# 환자 처방기록(병원 예약자 명단id(fk), 약국 예약자 명단id(fk), 처방 내용들)

# <환자 시스템 Table>
# 병원(이름, 위도, 경도, 시각(최근 간 병원), check(자주 간 병원 등록 유무))

# login 정보를 바탕으로 검색하여 
# 1) 정보가 없는 경우 
# 2) 있는 경우 
# 2-1) type이 없는 경우 
# 2-2)환자 타입 
# 2-3)병원 타입 
# 2-4)상점 타입
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
def hosp_list(lat, lng):
    lat = round(lat, 7)
    lng = round(lng, 7)
    print("@@@@@@@@@@@@@@")
    print(lat)
    print(lng)
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
    # pprint(params)
    r = requests.get(url, params=params)    # url에 parm정보추가
    # pprint(r)
    return r.json()          

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
      
def get_hosp(name):
    sql = f'''SELECT name
              FROM hosp_Info
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

def visited_record(local, domain):
    sql = f'''SELECT hospital_name, time
              FROM visited_record
              WHERE local=\'{local}\' and domain=\'{domain}\'
              ORDER BY time DESC
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
    json = hosp_list(lat, lng)
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
if __name__ == ("__main__"):
    lng = 127.0331892    # 파라미터로 받아오거나 한양대 위도,경도로 설정
    lat = 37.5585146
    pprint(hosp_list(lat, lng))
    # pprint(get_hosp_list())