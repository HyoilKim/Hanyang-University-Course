# db를 관리하는 code
import psycopg2 as pg
import psycopg2.extras
import json
import requests
from apicall import hosp_list
from pprint import pprint
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

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
                phone_number varchar(20) NOT NULL PRIMARY KEY,
                local varchar(20) NOT NULL,
                domain varchar(20) NOT NULL,
                password varchar(20) NOT NULL,
                type varchar(20) DEFAULT 'patient'
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
# 이름(name), 주소(addr), 위도(XPos), 경도(YPos), 거리(distance), 오픈시간, 처방가능여부
def create_pharmInfo_table():
    sql = f'''CREATE TABLE pharm_Info (
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
                prescribe_possible varchar(100) DEFAULT 'unknown'                
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
                patient_name varchar(20) NOT NULL,
                institution_name varchar(20) NOT NULL,
                date varchar(100) NOT NULL
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

# 즐겨찾는 병원 목록
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

# 예약 내역
def create_reservation_list_table():
    sql = f'''CREATE TABLE reservation_list (
                id SERIAL NOT NULL,
                name varchar(20) NOT NULL,
                phone_number varchar(20) NOT NULL,
                date varchar(20) NOT NULL,
                institution_name varchar(20) NOT NULL
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


# 발급 년월일 번호
# 환자 이름
# 병원 이름
# 처방의약품의 명칭, 1회투약량, 1일 투여횟수, 총투약일수
# 조제 연월일
# 병원 이름
# 처방 변경-수정-확인 내용
def create_description_list_table():
    sql = f'''CREATE TABLE prescription_list (
                id SERIAL NOT NULL,
                patient_name varchar(20),
                phone_number varchar(20),
                hospital_name varchar(100),
                hospital_date varchar(30),
                medicine_name varchar(20),
                amount_per_onetime integer,         
                count_per_oneday integer,
                how_long_day integer,
                pharmacy_date varchar(30),
                pharmacy_name varchar(100),
                pharmacy_opinion varchar(100),  
                pharmacy_status varchar(10) DEFAULT 'unknown'
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

def create_glass_store_table():
    sql = f'''CREATE TABLE glasses_store (
                lat double precision,
                lng double precision,
                name varchar(50),
                addr varchar(100),
                type varchar(10)
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


def create_glasses_description_table():
    sql = f'''CREATE TABLE glasses_description (
                id serial NOT NULL,
                hospital_date varchar(20),
                patient_name varchar(50),
                hospital_name varchar(50),
                r_vision varchar(10),
                l_vision varchar(10),
                fixed_r_vision varchar(10),
                fixed_l_vision varchar(10),
                galsses_date varchar(20),
                recommend_date varchar(20)
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
        
def init_glass_store_table():
    # 네이버 검색 결과
    res = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%ED%95%9C%EC%96%91%EB%8C%80+%EC%95%88%EA%B2%BD%EC%A0%90&oquery=%EC%95%88%EA%B2%BD%EC%A0%90&tqi=UQ55jsprvN8ssv165RZssssssNC-479615')
    soup = BeautifulSoup(res.content, 'html.parser')
    try:
        conn = pg.connect(connect_string) # DB연결(로그인)
        cur = conn.cursor() # DB 작업할 지시자 정하기
        for link in soup.find_all('a'):
            tmp = link.get('href')
            tmp = str(tmp)
            if 'lng' in tmp:
                idx = tmp.find('lat')
                lat = tmp[idx+4:idx+14]
                idx = tmp.find('lng')
                lng = tmp[idx+4:idx+14]
                type = "naver"
                sql = f'''INSERT INTO glasses_store(lat, lng, type)
                        VALUES (\'{lat}\', \'{lng}\', \'{type}\')
                '''
                cur.execute(sql)
                print(sql)
        cur.execute(sql) # sql 문을 실행
        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)

def nikon(page):
    url = 'http://www.nikon-lenswear.co.kr/assets/store-search-daum/com_list.php'
    params = {
        'sno': page,
        'location': 'a'
    }
    res = requests.get(url, params=params)

    try:
        conn = pg.connect(connect_string) # DB연결(로그인)
        cur = conn.cursor() # DB 작업할 지시자 정하기
        # res = requests.get('http://www.nikon-lenswear.co.kr/assets/store-search-daum/com_list.php?sno=2520&location=a&tmptitle=&title_like=&isee=')   
        soup = BeautifulSoup(res.content, 'html.parser')
        for link in soup.find_all('div'):
            link = str(link)
            if '서울' in link:
                tmp = link.split('\n')
                if len(tmp) == 8:
                    name = tmp[1]
                    name = name[5:]
                    idx = name.find('<')
                    name = name[:idx]

                    addr = tmp[2]
                    addr = addr[5:]
                    idx = addr.find('<')
                    addr = addr[:idx]
                    type = "nikon"
                    sql = f'''INSERT INTO glasses_store (name, addr, type)
                              VALUES (\'{name}\', \'{addr}\', \'{type}\');
                    ''' 
                    print(sql)
                    cur.execute(sql) 

        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)

if __name__ == "__main__":
    # create_customersInfo_table()
    # init_customersInfo_table()
    # create_hospInfo_table()
    # init_hospInfo_table()
    # create_visited_record_table()
    # add_visited_record()
    # create_favorite_hospital_table()
    # create_pharmInfo_table()
    # create_description_list_table()
    # create_reservation_list_table()
    # create_glass_store_table()
    # init_glass_store_table()
    # nikon(2510)
    # nikon(2520)
    # nikon(2430)
    # nikon(2540)
    create_glasses_description_table()
    