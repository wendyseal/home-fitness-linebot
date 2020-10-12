from linebot.models import (MessageAction, TextSendMessage,PostbackAction, QuickReply, QuickReplyButton)
from config import line_bot_api
from database.usertable import savebasic02,savebasic03,statelog,statelog_startdate,statelog_enddate,checkdate
from database.exercise import create_exerciselog01, create_exerciselog02
from flex.template_msg import buttons_template
from datetime import date
today = date.today()

def handle(event):
    user_id = event.source.user_id


    Ans_gender=['gender=male','gender=female','gender=other']
    Ans_frequency = ['f=high', 'f=middle', 'f=low']
    if event.postback.data in Ans_gender:
        gender = event.postback.data.split('=')[1]
        text_quickreply0 = QuickReplyButton(action=PostbackAction(label='一周3次以上', display_text='常常~', data='f=high'))
        text_quickreply1 = QuickReplyButton(action=PostbackAction(label='一周1-2次', display_text='偶爾~', data='f=middle'))
        text_quickreply2 = QuickReplyButton(action=PostbackAction(label='沒有運動', display_text='幾乎沒在運動~', data='f=low'))
        quick_reply_array2 = QuickReply(items=[text_quickreply0, text_quickreply1, text_quickreply2])
        reply_text_message2 = TextSendMessage('平常的運動習慣?', quick_reply=quick_reply_array2)
        line_bot_api.reply_message(event.reply_token, [reply_text_message2])
        savebasic02(user_id,gender)
        print(event.postback.data)

    elif event.postback.data in Ans_frequency:
        frequency = event.postback.data.split('=')[1]
        text_quickreply0 = QuickReplyButton(action=MessageAction(label="健康", text="一切都很好，放馬過來吧！ᕦ(ò_óˇ)ᕤ"))
        text_quickreply1 = QuickReplyButton(action=MessageAction(label="不太好", text="啊啊⋯有點累"))
        quick_reply_array3 = QuickReply(items=[text_quickreply0, text_quickreply1])
        reply_text_message3 = TextSendMessage("有睡飽嗎？身體有沒有哪裡不舒服？", quick_reply=quick_reply_array3)
        line_bot_api.reply_message(event.reply_token, [reply_text_message3])
        savebasic03(user_id, frequency)
        print(event.postback.data)
    # 詢問基本資料=================================================================




    # 運動日誌-新增日誌=================================================================
#=>選完日期後回傳的資料
#=>database.usertable.statelog() 紀錄狀態 加入日期
#=>database.exercise.create_exerciselog01(user_id, datestr)更新exercise表格的date
#=>發送訊息:請輸入當天運動紀錄
    elif "q1" == event.postback.data:
        user_id = event.source.user_id
        datestr=(event.postback.params['date'])
        print("新增日誌中，收到回傳日期:",event.postback.params['date'])
        create_exerciselog01(user_id, datestr)
        statelog(user_id, datestr)
        # # recordtime=time.strftime(datestr, "%Y-%m-%d")
        # print(recordtime)
        textmessage = f"請輸入{event.postback.params['date']}當天的運動紀錄"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=textmessage))

    # 運動日誌-查詢日誌=================================================================
#查詢日誌 我希望起始&結束日期的buttom都按過
    # =>寫入usertables:  tatelog_enddate(user_id, enddate)
    # 查詢完會把日期資料start_date & end_date刪掉
    elif ('startdate' ==  event.postback.data) or ('enddate'==event.postback.data) :
        if 'startdate' ==  event.postback.data :
            startdate=event.postback.params['date']
            statelog_startdate(user_id, startdate)
            print("已成功寫入startdate")
            # result = checkdate(user_id)
            # if "Y" in result[0]:
            #     startdate=result[2]
            #     enddate=result[3]
            # elif "N" in result[0]:
            #     text=result[1]
            # check=checkdate(user_id)
            # text=check[1]
            # startdate = check[2]
            # print(check)
            # enddate=check[3]
            # buttons_template(today, user_id,check)
            print("已成功寫入enddate")
            check = checkdate(user_id)
            if "search=Y" in check[0]:
                startdate = check[1]
                enddate = check[2]
                print("兩者皆已更新")
                textmessage = f"查詢{startdate}至{enddate}的運動日誌，是否正確?"

                text_quickreply0 = QuickReplyButton(action=MessageAction(label="正確", text="對，確認查詢~"))
                text_quickreply1 = QuickReplyButton(action=MessageAction(label="重新選擇日期", text="錯了，我想重新選擇日期~"))
                quick_reply_array3 = QuickReply(items=[text_quickreply0, text_quickreply1])
                reply_text_message3 = TextSendMessage(textmessage, quick_reply=quick_reply_array3)
                line_bot_api.reply_message(event.reply_token, [reply_text_message3])

        elif 'enddate'== event.postback.data :
            enddate=event.postback.params['date']
            statelog_enddate(user_id, enddate)
            print("已成功寫入enddate")
            check = checkdate(user_id)
            if "search=Y" in check[0]:
                startdate = check[1]
                enddate = check[2]
                print("兩者皆已更新")
                textmessage = f"查詢{startdate}至{enddate}的運動日誌，是否正確?"

                text_quickreply0 = QuickReplyButton(action=MessageAction(label="正確", text="對，確認查詢~"))
                text_quickreply1 = QuickReplyButton(action=MessageAction(label="重新選擇日期", text="錯了，我想重新選擇日期~"))
                quick_reply_array3 = QuickReply(items=[text_quickreply0, text_quickreply1])
                reply_text_message3 = TextSendMessage(textmessage, quick_reply=quick_reply_array3)
                line_bot_api.reply_message(event.reply_token, [reply_text_message3])


            # result = checkdate(user_id)
            # if "Y" in result[0]:
            #     startdate=result[2]
            #     enddate=result[3]
            # elif "N" in result[0]:
            #     text=result[1]
            ##輸入訊息檢查state狀態，如果有日期，是Y 沒有是N
            ##輸入訊息檢查state狀態，如果有日期，是Y 沒有是N
    #
    #     elif "search=Noenddate" ==check[0]:
    #         startdate = event.postback.params['date']
    #         statelog_startdate(user_id, startdate)
    #         print("已成功寫入startdate")
    #         textmessage = check[1]
    #         line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=textmessage)])
    #
    #     elif "search=Nostartdate" == check[0]:
    #         textmessage = check[1]
    #         enddate = event.postback.params['date']
    #         statelog_enddate(user_id, enddate)
    #         print("已成功寫入enddate")
    #         line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=textmessage)])



#確定要記錄日誌##################
# 新增紀錄-3 使用者不要更新
    elif "update=N" in event.postback.data:
        text_quickreply0 = QuickReplyButton(action=MessageAction(label="新增紀錄", text="新增紀錄"))
        text_quickreply1 = QuickReplyButton(action=MessageAction(label="查詢紀錄", text="查詢紀錄"))
        text_quickreply2 = QuickReplyButton(action=MessageAction(label="不用了", text="不用了"))
        quick_reply_array = QuickReply(items=[text_quickreply0, text_quickreply1,text_quickreply2])
        reply_text_message = TextSendMessage("好的，還需要新增運動日誌或查詢紀錄嗎?", quick_reply=quick_reply_array)
        line_bot_api.reply_message(event.reply_token, [reply_text_message])

# 新增紀錄-3 寫入database.exercise的record欄位
    elif "update=Y" in event.postback.data:
        print(event.postback.data,"type",type(event.postback.data))
        date=event.postback.data.split(",")[1]
        date=date.split("=")[1]
        record = event.postback.data.split(",")[2]
        record=record.split("=")[1]
        textmessage=create_exerciselog02(user_id, date, record)
        text_quickreply0 = QuickReplyButton(action=MessageAction(label="新增紀錄", text="新增紀錄"))
        text_quickreply1 = QuickReplyButton(action=MessageAction(label="查詢紀錄", text="查詢紀錄"))
        text_quickreply2 = QuickReplyButton(action=MessageAction(label="不用了", text="不用了"))
        quick_reply_array = QuickReply(items=[text_quickreply0, text_quickreply1, text_quickreply2])
        reply_text_message = TextSendMessage("需要繼續新增運動日誌或查詢紀錄嗎?", quick_reply=quick_reply_array)
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=textmessage),reply_text_message])

    return "postback_event done"
    # 新增日誌完成!!!!!!=================================================================









