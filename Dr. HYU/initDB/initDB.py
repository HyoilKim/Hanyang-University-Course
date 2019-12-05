# db를 관리하는 code
import psycopg2 as pg
import psycopg2.extras
import json
import requests
from apicall import hosp_list
from pprint import pprint
from datetime import datetime

pg_local = {
    'host': "localhost", # localhost
    'user': "postgres",  # dbuser
    'dbname': "postgres",  # dbapp
    'password': "gydlf1894*"     
}
db_connector = pg_local
connect_string = "host={host} user={user} dbname={dbname} password={password}".format(
    **db_connector)   


# - 정적인 정보들 - 
# <회원 정보 Table>
# 이메일, 비밀번호, 타입(환자, 병원관리자, 상점주인)

# <병원 정보 Table>
# 위도, 경도, 진료시간, 의원 수, 진료 과목, 이름, 주소

# <약국 정보 Table>
# 위도, 경도, 처방시간(from 0 to 24), 이름, 주소,

# id, 이름, 휴대폰 번호를 가지는 Table 생성
def create_customersInfo_table():
    sql = f'''CREATE TABLE customers_Info (
                id SERIAL NOT NULL,
                name varchar(20) NOT NULL,
                phone_number integer NOT NULL PRIMARY KEY,
                local varchar(20) NOT NULL,
                domain varchar(20) NOT NULL,
                password varchar(20) NOT NULL,
                type varchar(20) DEFAULT 'no Type'
            );
    '''
    try:
        conn = pg.connect(connect_string) # DB연결(로그인)
        cur = conn.cursor() # DB 작업할 지시자 정하기
        print(sql)
        cur.execute(sql) # sql 문을 실행
        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)

# customers정보 초기화
def init_customersInfo_table():
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        f = open("C:\\Users\\Public\\customers.csv", "r", encoding='UTF-8')
        for line in f:
            tmp = line.split(',')
            name = tmp[0]
            phone_number = tmp[1]
            local = tmp[2]
            domain = tmp[3]
            password = tmp[4]
            lat = tmp[len(tmp)-2]
            tmp = tmp[len(tmp)-1].split('\n')
            lng = tmp[0]
            print(lng)
            
            sql = f'''INSERT INTO customers_Info(name, phone_number, local, domain, password)
                      VALUES (\'{name}\', \'{phone_number}\', \'{local}\'
                                    , \'{domain}\', \'{password}\');
            '''
            print(sql)
            cur.execute(sql)
        f.close()
        conn.commit()
        conn.close()
        # print(sql)
    except pg.OperationalError as e:
        print(e)
        return -1
    return 1;


# 전문의 의원 수(doctor_cnt), 진료 과목(diagnosis_kinds), 이름(name), 주소(addr), 위도(XPos), 경도(YPos), 거리(distance)
def create_hospInfo_table():
    sql = f'''CREATE TABLE hosp_Info (
                id SERIAL NOT NULL,
                name varchar(100) NOT NULL PRIMARY KEY,
                addr varchar(100) NOT NULL,
                lat double precision NOT NULL,
                lng double precision NOT NULL,
                distance double precision NOT NULL,
                weekday_open integer NOT NULL,
                weekday_close integer NOT NULL,
                weekend_open integer NOT NULL,
                weekend_close integer NOT NULL,
                doctor_cnt integer NOT NULL,
                diagnosis_kinds varchar(100) NOT NULL
            );
    '''
    try:
        conn = pg.connect(connect_string) # DB연결(로그인)
        cur = conn.cursor() # DB 작업할 지시자 정하기
        print(sql)
        cur.execute(sql) # sql 문을 실행
        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)

# 병원 정보 Table
def init_hospInfo_table():
    json = hosp_list()
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

# 약국 정보 테이블
# 이름(name), 주소(addr), 위도(XPos), 경도(YPos), 거리(distance)
def create_hospInfo_table():
    sql = f'''CREATE TABLE hosp_Info (
                id SERIAL NOT NULL,
                name varchar(100) NOT NULL PRIMARY KEY,
                addr varchar(100) NOT NULL,
                lat double precision NOT NULL,
                lng double precision NOT NULL,
                distance double precision NOT NULL,
                weekday_open integer NOT NULL,
                weekday_close integer NOT NULL,
                weekend_open integer NOT NULL,
                weekend_close integer NOT NULL,
                doctor_cnt integer NOT NULL,
                diagnosis_kinds varchar(100) NOT NULL
            );
    '''
    try:
        conn = pg.connect(connect_string) # DB연결(로그인)
        cur = conn.cursor() # DB 작업할 지시자 정하기
        print(sql)
        cur.execute(sql) # sql 문을 실행
        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)

# 약국 정보 Table
def init_hospInfo_table():
    json = hosp_list()
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

# 환자 방문 기록
def create_visited_record_table():
    sql = f'''CREATE TABLE visited_record (
                id SERIAL NOT NULL,
                hospital_name varchar(20) NOT NULL,
                time varchar(100) NOT NULL,
                local varchar(20) NOT NULL,
                domain varchar(20) NOT NULL
            );
    '''
    try:
        conn = pg.connect(connect_string) # DB연결(로그인)
        cur = conn.cursor() # DB 작업할 지시자 정하기
        print(sql)
        cur.execute(sql) # sql 문을 실행
        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)
        
# 방문 기록 추가
def add_visited_record():
    hospital_name = "서울성심병원"
    time = "2019-07-15"
    local = "tfalkc"
    domain = "smh.com.au"
    sql = f'''INSERT INTO visited_record(hospital_name, time, local, domain)
                      VALUES (\'{hospital_name}\', \'{time}\', \'{local}\', \'{domain}\');
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

# 환자의 즐겨찾는 병원 목록
def create_favorite_hospital_table():
    sql = f'''CREATE TABLE favorite_hospital (
                id SERIAL NOT NULL,
                hospital_name varchar(20) NOT NULL,
                local varchar(20) NOT NULL,
                domain varchar(20) NOT NULL
            );
    '''
    try:
        conn = pg.connect(connect_string) # DB연결(로그인)
        cur = conn.cursor() # DB 작업할 지시자 정하기
        print(sql)
        cur.execute(sql) # sql 문을 실행
        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)
# 환자 처방 기록(환자, 병원이름, 처방내용...)
# 즐겨찾는 병원 목록(환자, 병원이름)
if __name__ == "__main__":
    # create_customersInfo_table()
    # init_customersInfo_table()
    # create_hospInfo_table()
    # init_hospInfo_table()
    # create_visited_record_table()
    # add_visited_record()
    create_favorite_hospital_table()

