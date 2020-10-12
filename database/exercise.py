import psycopg2
from datetime import datetime,timedelta,date
from prettytable import PrettyTable
from prettytable import from_db_cursor


# 運動日誌-新增日誌=================================================================
def create_exerciselog01(user_id, date):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    SQL = "INSERT INTO exercise (user_id, date) VALUES (%s, %s)"
    data = (user_id, date)
    try:
        cur.execute(SQL, data)
        conn.commit()
        print(f"========新增日誌中，已選擇日期並寫入exercise-date=========")
    except psycopg2.DatabaseError as error:
        print(f'Error{error}')
    conn.close()

#在message中呼叫
def updatecheck(user_id, date):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    SQL2 = f"select id, date, record from exercise WHERE user_id= '{user_id}' and date='{date}' order by id DESC"
    cur.execute(SQL2)
    cur_list = []
    for i in cur.fetchall():
        cur_list.append(i)
        print(i)
    print("cur_list:",cur_list[0])
    last_record=list(cur_list[0])[2] #record
    print("從database.exercise.updatecheck(user_id, date)確認 exercise的record欄位是不是空的，避免重複寫入")
    print("結果在這邊last_record:",last_record,"type(last_record):",type(last_record))
    conn.close()
    return last_record


#在postback中呼叫
def create_exerciselog02(user_id, date, record):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    SQL1 = f"select id, record from exercise WHERE user_id= '{user_id}' and date='{date}' ORDER by id DESC ;"
    cur.execute(SQL1)
    resultlist = []
    for i in cur.fetchall():
        resultlist.append(i)
        print(i)
    print("resultlist:",resultlist)
    if type(resultlist[0])==None:
        print("(cur.fetchone())==None")
        text = "紀錄失敗Q^Q"
        pass
    else:
        print("resultlist:",resultlist)
        id=list(resultlist[0])[0]
        print("id",id)
        print(f"成功透過date找到最新一筆id={id}")
        print(f"====開始寫入此筆運動日誌record")
        #如果以後 exercise表內的欄位改變 [3]可能也要更新
        sql2 = f"UPDATE exercise SET record = '{record}' WHERE user_id= '{user_id}' and id={id}"
        try:
            cur.execute(sql2)
            conn.commit()
            print(f"====================YA成功新增1筆運動日誌資料{record},id={id}，動作終止==========================")
        except psycopg2.DatabaseError as error:
            print(f'Error{error}')
        conn.close()
        text="完成紀錄囉!"
    return text


#更新日誌
def updatelog(user_id,id,record):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    sql1 = f"UPDATE exercise SET record = '{record}' WHERE user_id='{user_id}'and id={id}"
    try:
        cur.execute(sql1)
        conn.commit()
        print(f"====================更新exercise{id}==========================")
        text = "完成紀錄更新囉!"
    except psycopg2.DatabaseError as error:
        print(f'Error{error}')
        text = "更新失敗Q^Q"
    conn.close()
    print(text)
    return text

def deletelog(user_id,id):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    sql1 = f"delete from exercise WHERE user_id='{user_id}'and id={id}"
    try:
        cur.execute(sql1)
        conn.commit()
        print(f"====================刪除exercise{id}==========================")
        text = "成功刪除紀錄囉!"
    except psycopg2.DatabaseError as error:
        print(f'Error{error}')
        text = "刪除紀錄失敗Q^Q"
    conn.close()
    print(text)
    return text

#查詢日誌
def search_exerciselog(user_id, startdate, enddate):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    SQL2 = f"select id, date, record from exercise ORDER BY id ASC WHERE user_id= '{user_id}' and date<='{enddate}' and date>='{startdate}'"
    cur.execute(SQL2)
    print()
    table=from_db_cursor(cur)
    # table.get_string(sortby='id', sort_key=lambda row:int(row[0]))
    # cur_list=[]
    # for i in cur.fetchall():
    #     cur_list.append(i)
    #     print(i)
    # print(cur_list,"=====")
    conn.close()
    return table
#查詢單筆日誌
def search_onelog(user_id,id):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    SQL2 = f"select date, record from exercise WHERE user_id= '{user_id}' and id='{id}'"
    cur.execute(SQL2)
    cur_list=[]
    for i in cur.fetchone():
        cur_list.append(i)
        print(i)
    print(cur_list,"=====")
    date=cur_list[0]
    record=cur_list[1]
    print(date,record)
    conn.close()
    return date,record