import psycopg2 as pg
import psycopg2.extras
import json
import requests
from apicall import hosp_list, test1
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
        
        

if __name__ == ("__main__"):
    pprint(hosp_list())