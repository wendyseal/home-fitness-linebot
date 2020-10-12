import psycopg2
from datetime import datetime,timedelta,date
from prettytable import PrettyTable
from prettytable import from_db_cursor
import time
# today=datetime.now()
# print(today)
# print(type(today))
# today=datetime.strftime(datetime.now(),'%Y-%m-%d')
# print(today)
# print(type(today))
# today=date(datetime.now()
# print(today)
# print(type(today))
#查詢過去7天的運動次數
def count_exercise(user_id,range):
    today = date.today()
    diff=timedelta(days=range) #range 是7或30
    firstday = today-diff
    today=str(today)
    firstday=str(firstday)
    print(firstday,"至" ,today)
    conn = psycopg2.connect(database="postgres", user="wendy", password="qazwsx", host="34.80.156.226", port="5432")
    cur = conn.cursor()

    SQL1 = f"select count (*) from exercise ORDER BY id ASC WHERE user_id= '{user_id}' and date<='{today}' and date>='{firstday}'"
    cur.execute(SQL1)
    cur_result = cur.fetchone()
    print(cur_result)
    count=list(cur_result)[0]
    # result=f"{range}天內，運動了{count}次"

    SQL2 = f"select id, date, record from exercise WHERE user_id= '{user_id}' and date<='{today}' and date>='{firstday}'"
    cur.execute(SQL2)
    table=from_db_cursor(cur)
    # table.get_string(sortby='id', sort_key=lambda row: int(row[0]))

    # cur_list=[]
    # for i in cur.fetchall():
    #     cur_list.append(i)
    #     print(i)
    # print(cur_list)
    # count=list(cur_result)[0]

    conn.close()
    return range,count,table,firstday,today
    # table = PrettyTable(['流水號', '運動日期', '運動日誌'])
    # table.add_row(['1', 'server01', '服务器01', '172.16.0.1'])
    # table.add_row(['2', 'server02', '服务器02', '172.16.0.2'])
    # table.add_row(['3', 'server03', '服务器03', '172.16.0.3'])
    # table.add_row(['4', 'server04', '服务器04', '172.16.0.4'])
    # table.add_row(['5', 'server05', '服务器05', '172.16.0.5'])
    # table.add_row(['6', 'server06', '服务器06', '172.16.0.6'])
    # table.add_row(['7', 'server07', '服务器07', '172.16.0.7'])
    # table.add_row(['8', 'server08', '服务器08', '172.16.0.8'])
    # table.add_row(['9', 'server09', '服务器09', '172.16.0.9'])
    # print(table)
    #
    #
    # SQL1 = f"UPDATE rank SET (weektimes, weekrank, montimes, monrank) VALUES (%s, %s, %s, %s) WHERE user_id= {user_id};"
    # data1 = (weektimes, weekrank, montimes, monrank)
    # try:
    #     cur.execute(SQL, data)
    #     conn.commit()
    #     print(f"====================更新rank資料==========================")
    # except psycopg2.DatabaseError as error:
    #     print(f'Error{error}')
    # conn.close()

#查詢過去30天的運動次數
