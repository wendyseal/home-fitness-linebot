import psycopg2
from linebot.models import (MessageAction, TextSendMessage,PostbackAction, QuickReply, QuickReplyButton)
from config import line_bot_api


# 詢問基本資料=================================================================
def savebasic01(user_id, display_name, picture_url):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    print('Connection successful!')
    # 檢查使用者有沒有建立過資料
    sql = f"SELECT user_id from public.usertable WHERE user_id='{user_id}'"
    cur.execute(sql)
    record = cur.fetchone()
    print(record)
    print(type(record))
    if record==None:
        print('record==None 123')
        sql2 = "INSERT INTO usertable (user_id, display_name, picture_url) VALUES (%s, %s, %s)"
        data2 = (str(user_id), str(display_name), str(picture_url))
        print('to INSERT INTO')
        try:
            cur.execute(sql2, data2)
            conn.commit()
            print(f"====================新增1筆user資料==========================")
        except psycopg2.DatabaseError as error:
            print(f'Error{error}')
        # 順便建立使用者rank表的初始值
        sql3 = "INSERT INTO rank (user_id, weektimes, weekrank, montimes, monrank) VALUES (%s, %s, %s, %s, %s)"
        data3 = (str(user_id), 0, '尚未開始記錄', 0, '尚未開始記錄')
        cur.execute(sql3, data3)
        conn.commit()
        print('寫入 新增成功')
    else:
        sql1 = f"UPDATE usertable SET (display_name, picture_url) = ('{display_name}','{picture_url}') WHERE user_id='{user_id}'"
        try:
            cur.execute(sql1)
            conn.commit()
            print(f"====================更新user基本資料(暱稱、照片)==========================")
        except psycopg2.DatabaseError as error:
            print(f'Error{error}')
        print('更新成功')
    conn.close()

def savebasic02(user_id, gender):
    conn = psycopg2.connect(database='postgres', user='wendy', password='qazwsx', host='34.80.156.226', port="5432")
    cur = conn.cursor()
    print('Connection successful!')
    sql = f"UPDATE usertable SET gender = '{gender}' WHERE user_id= '{user_id}'"
    try:
        cur.execute(sql)
        conn.commit()
        print(f"====================更新user基本資料(性別、運動頻率)==========================")
    except psycopg2.DatabaseError as error:
        print(f'Error{error}')
    conn.close()

def savebasic03(user_id, frequency):
    conn = psycopg2.connect(database='postgres', user='wendy', password='qazwsx', host='34.80.156.226', port="5432")
    cur = conn.cursor()
    print('Connection successful!')
    sql = f"UPDATE usertable SET frequency = '{frequency}' WHERE user_id= '{user_id}'"
    try:
        cur.execute(sql)
        conn.commit()
        print(f"====================更新user基本資料(性別、運動頻率)==========================")
    except psycopg2.DatabaseError as error:
        print(f'Error{error}')
    conn.close()


    #運動日誌-新增日誌=================================================================
def statelog(user_id, datestr):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    sql = f"UPDATE usertable SET state = '{datestr}' WHERE user_id= '{user_id}'"
    try:
        cur.execute(sql)
        conn.commit()
        print(f"========新增日誌中，已選擇日期並寫入usertable-state=========")
    except psycopg2.DatabaseError as error:
        print(f'Error{error}')
    conn.close()

#一旦輸入文字 就會觸發 -先檢查User狀態=>message
def checkstate(user_id):
    conn = psycopg2.connect(database='postgres', user='wendy', password='qazwsx', host='34.80.156.226', port="5432")
    cur = conn.cursor()
    sql = f"SELECT state from public.usertable WHERE user_id='{user_id}'"
    cur.execute(sql)
    result = cur.fetchone()
    print("cur.fetchone():",result)
    if result == None:
        result = "checkstate=N"
        print(f"========新增日誌中，已輸入日誌內容，查無usertable-state的日期紀錄，動作終止=========")
        conn.close()
        pass
    else:
        result_list=list(result)
        date=result_list[0]
        print("date:",date)
        print("type(date):",type(date))
        result = f"checkstate=Y,{date}"
        print(f"========新增日誌中，已輸入日誌內容，並查詢usertable-state的日期=========")
        conn.close()
    return result

#運動日誌-查詢日誌=================================================================
##紀錄選取的起始&結束日期
def statelog_startdate(user_id, startdate):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    sql = f"UPDATE usertable SET start_date = '{startdate}' WHERE user_id= '{user_id}'"
    try:
        cur.execute(sql)
        conn.commit()
        print(f"===查詢日誌中，已更新start_date資料===")
    except psycopg2.DatabaseError as error:
        print(f'Error{error}')
    conn.close()

def statelog_enddate(user_id, enddate):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    sql = f"UPDATE usertable SET end_date = '{enddate}' WHERE user_id= '{user_id}'"
    try:
        cur.execute(sql)
        conn.commit()
        print(f"===查詢日誌中，已更新end_date資料===")
    except psycopg2.DatabaseError as error:
        print(f'Error{error}')
    conn.close()

# # 查詢紀錄-2 日期確認 確定起始&結束日期都有選擇
# =>傳回str型態的文字
def checkdate(user_id):
    conn = psycopg2.connect(database='postgres', user='wendy', password='qazwsx', host='34.80.156.226', port="5432")
    cur = conn.cursor()
    sql = f"select start_date, end_date from public.usertable WHERE user_id='{user_id}'"
    cur.execute(sql)
    result = cur.fetchone()
    result_l=list(result)
    # print("result:", result_l)
    startdate = result_l[0]
    enddate = result_l[1]
    if startdate == None and enddate == None:
        result = ["search=Noall","請選取起始&結束日期~~"]
        conn.close()
        pass
    elif startdate == None:
        result = ["search=Nostart","請選取起始日期~~",enddate]
        conn.close()
        pass
    elif enddate == None:
        result = ["search=Noend","請選取結束日期~~",startdate]
        conn.close()
        pass
    else:
        print("startdate:", startdate)
        print("enddate:", enddate)
        result = ["search=Y",startdate,enddate]
        conn.close()
    return result

def deletedate(user_id):
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()
    sql1 = f"UPDATE usertable SET (start_date, end_date) = (null,null) WHERE user_id='{user_id}'"
    try:
        cur.execute(sql1)
        conn.commit()
        print(f"====================更新user 查詢日期==========================")
    except psycopg2.DatabaseError as error:
        print(f'Error{error}')
    print('更新成功')

