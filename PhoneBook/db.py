# db를 관리하는 code
import psycopg2 as pg
import psycopg2.extras

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

# id, 이름, 휴대폰 번호를 가지는 Table 생성
def create_table(table_name):
    sql = f'''CREATE TABLE {table_name} (
                id SERIAL NOT NULL,
                name varchar(20),
                number varchar(20)
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

# contact.csv에 있는 이름과 전화번호를 가져와 db를 초기화
def init_table():
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        #
        f = open("C:\\Users\\Public\\miniconda\\hw2\\src\\flask\\contact.csv", "r")
        for line in f:
            # ,제거 하여 name, number 구분
            tmp = line.split(',')
            name = tmp[0]
            # tmp[1]이 개행을 포함하기 때문에 개행제거
            tmp = tmp[1].split('\n')
            number = tmp[0]        
            db_insert(name, number)
            sql = f'''INSERT INTO phonebook1(name, number)
              VALUES (\'{name}\', \'{number}\');
            '''
            cur.execute(sql)
        f.close()
        conn.commit()
        conn.close()
        # print(sql)
    except pg.OperationalError as e:
        print(e)
        return -1
    return 1;

# web form에서 입력받은 이름과 전화번호를 db에 추가
def db_insert(name, number):
    sql = f'''INSERT INTO phonebook1(name, number)
              VALUES (\'{name}\', \'{number}\');
           '''
    try:
        conn = pg.connect(connect_string)
        cur = conn.cursor() 
        cur.execute(sql)
        conn.commit()
        conn.close()
        # print(sql)
    except pg.OperationalError as e:
        print(e)
        return -1
    return 1;

# web form에서 입력받은 이름으로 시작하는 정보와 같은 성의 수를 출력
def db_search(name):
    # name으로 시작하는 이름을 포함하는 rows  ex) nmae = 홍길 -> 홍삼 검색 되지 않음      
    searchNameSQL = f'''SELECT name, number 
                        FROM phonebook1 
                        WHERE name LIKE \'{name}%\'; 
           '''
    # name의 성으로 시작하는 이름의 수 ex) name = 홍길 -> 홍삼은 count되어야함
    countNameSQL = f'''SELECT COUNT(*) AS count 
                       FROM phonebook1 
                       WHERE name LIKE \'{name[0]}%\'; 
                     '''
    print(countNameSQL)
    try:
        conn = pg.connect(connect_string) 
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) # cursor_factory뭔지 ?      
        cur.execute(searchNameSQL) 
        result = cur.fetchall()
        cur.execute(countNameSQL)
        tmp = cur.fetchall()
        # print(result)
        # print(tmp)
        # 검색 내용이 존재 하지 않을 경우
        if(result == []) :
            print("검색내용 없음")
            res = [{}]
            res[0]['name'] = "x"
            res[0]['number'] = "x"
            res[0]['count'] = tmp[0]['count']
            return res
        else :
            print("검색내용 있음")
            result[0]['count'] = tmp[0]['count']  
        conn.commit()
        conn.close()
        return result
    except Exception as e:
        print(e)
        return []    

# name, number를 가지는 id의 row하나만 삭제
def db_delete(name, number):
    deleteRowSQL = f'''DELETE
                       FROM phonebook1
                       WHERE id IN (
                           SELECT id 
                           FROM phonebook1
                           WHERE name = \'{name}\' and number = \'{number}\' 
                           LIMIT 1
                       )
                    '''
    try:
        conn = pg.connect(connect_string) # DB연결(로그인)
        cur = conn.cursor() # DB 작업할 지시자 정하기
        cur.execute(deleteRowSQL) # sql 문을 실행
        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)
        return -1
    return 1;

# name, number를 가지고 있는 row의 number를 new_number로 변환
def db_update(name, number, new_number):
    # \'{문자}\', {숫자}
    sql = f'''UPDATE phonebook1 
              SET number=\'{new_number}\'
              WHERE number=\'{number}\' and name=\'{name}\';
           '''
    print(sql)
    try:
        conn = pg.connect(connect_string) 
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
    except pg.OperationalError as e:
        print(e)
        return -1
    return 1;