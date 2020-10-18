import json
import os
from linebot.models import (FlexSendMessage, TextSendMessage, TemplateSendMessage, QuickReplyButton, QuickReply,
                            PostbackAction,MessageAction)
from config import line_bot_api
from database.exercise import updatecheck,search_exerciselog,updatelog,deletelog,search_onelog
from database.rank import count_exercise
from database.usertable import checkstate,deletedate,checkdate

from flex.template_msg import buttons_template,buttons_templatenewdate
from datetime import date


rich_menu_id01 ="richmenu-6751b6c408e76782f9abedf0625c894e"
rich_menu_id02 ="richmenu-01b7846ff426cbce7096eb905589aab4"
today = date.today()
#切換圖文選單 / 詢問基本資料 / 健身影片推薦 / 運動日誌  (查看&編輯: 新增/查詢/更新/刪除)
#圖文選單ID

def handle(event, rich_menu_id01=rich_menu_id01,rich_menu_id02=rich_menu_id02,today=today):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    msg_content = event.message.text
    check = checkdate(user_id)
    print(check[0])
    #詢問基本資料=================================================================
    if(event.message.text.find('一切都很好，放馬過來吧！ᕦ(ò_óˇ)ᕤ'or '健康')!= -1):
        start_textmessage = '瞭解～那麼我們開始今天的練習吧(^_−)−☆ 請點擊下方的圖文選單'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=start_textmessage))
        try:
            line_bot_api.link_rich_menu_to_user(
                user_id=event.source.user_id,
                rich_menu_id=rich_menu_id01
            )
            print('Success')
        except Exception as e:
            print(e)

    elif (event.message.text.find('啊啊⋯有點累'or '不太好')!= -1):
        start_textmessage = '瞭解～請不要太勉強自己，適度動一動即可。那麼讓我們開始今天的練習吧(^_−)−☆ 請點擊下方的圖文選單'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=start_textmessage))
        rich_menu_id01 = 'richmenu-6751b6c408e76782f9abedf0625c894e'
        try:
            line_bot_api.link_rich_menu_to_user(
                user_id=event.source.user_id,
                rich_menu_id=rich_menu_id01
            )
            print('Success')
        except Exception as e:
            print(e)

    #健身影片推薦=================================================================
    elif (event.message.text.find('我想練胸肌')!= -1):
        with open("./flex/c_push-up.txt", "r", encoding='utf8') as jsonfile:
            json_object = json.load(jsonfile)
        FM = FlexSendMessage.new_from_json_dict(json_object)
        # send_textmsg = TextSendMessage(text="你好我溫蒂")
        # line_bot_api.reply_message(controller.reply_token, [FM, send_textmsg])
        line_bot_api.reply_message(event.reply_token, FM)
    elif (event.message.text.find('我要消除鮪魚肚')!= -1) :
        with open(os.path.join(os.getcwd(),"flex","a_10mins_woman.txt"), "r", encoding='utf8') as jsonfile:
            json_object = json.load(jsonfile)
        FM = FlexSendMessage.new_from_json_dict(json_object)
        line_bot_api.reply_message(event.reply_token, FM)

    elif (event.message.text.find('想當背影Killer')!= -1):
        '''
        用JSON生成模板消息
            讀取本地的json檔案- json.load 取得json物件
            將json物件放入TemplateSendMessage的new_from_json_dict方法，並存在變數內即可
        '''
        print("有進入elif迴圈")
        with open(os.path.join(os.getcwd(),"flex","b_all_back_movement.json"), "r", encoding='utf8') as jsonfile:
            json_object = json.load(jsonfile)
        b01 = FlexSendMessage.new_from_json_dict(json_object)
        # with open(os.path.join(os.getcwd(),"flex","b_bird-dog.json"), "r", encoding='utf8') as jsonfile:
        #     json_object = json.load(jsonfile)
        # b02 = FlexSendMessage.new_from_json_dict(json_object)
        # with open(os.path.join(os.getcwd(),"flex","b_10mins_woman.json"), "r", encoding='utf8') as jsonfile:
        #     json_object = json.load(jsonfile)
        # b03 = FlexSendMessage.new_from_json_dict(json_object)
        # line_bot_api.reply_message(event.reply_token,[b01, b02, b03])
        line_bot_api.reply_message(event.reply_token,b01)

    elif (event.message.text.find('我想練臀腿')!= -1):
    # elif ('我想練臀腿') in controller.message.text:
        with open(os.path.join(os.getcwd(), "flex", "a_10mins_woman.txt"), "r", encoding='utf8') as jsonfile:
            json_object = json.load(jsonfile)
        FM = FlexSendMessage.new_from_json_dict(json_object)
        line_bot_api.reply_message(event.reply_token, FM)
        with open("flex/h_12mins_woman.json", "r", encoding='utf8') as jsonfile:
            json_object = json.load(jsonfile)
        FM = FlexSendMessage.new_from_json_dict(json_object)
        line_bot_api.reply_message(event.reply_token, FM)
    #切換圖文選單=================================================================
    elif ('編輯紀錄') == (event.message.text):
        line_bot_api.link_rich_menu_to_user(
            user_id=user_id,
            rich_menu_id=rich_menu_id02)
    elif ('回主選單') in (event.message.text):
        line_bot_api.link_rich_menu_to_user(
            user_id=user_id,
            rich_menu_id=rich_menu_id01
        )

    #運動日誌-新增紀錄=================================================================
## 新增紀錄-1
    elif ('新增紀錄') == (event.message.text):
        textmessage = '請選擇運動日期~٩(๑❛ᴗ❛๑)۶'
        replydatepicker = buttons_templatenewdate(today)#\[TextSendMessage(text=textmessage)
        line_bot_api.reply_message(event.reply_token, [replydatepicker])

# 查詢紀錄-1 =>查詢/更新/刪除 =>選擇日期 flex.template_msg.buttons_template=>postback
#     elif ('查詢紀錄') or ('更新紀錄') or(' 刪除紀錄') in (event.message.text):
    elif ('查詢紀錄') == (event.message.text):
        line_bot_api.reply_message(event.reply_token, buttons_template(today,user_id))
    elif  ('更新紀錄') == (event.message.text):
        line_bot_api.reply_message(event.reply_token, buttons_template(today,user_id))
    elif ('刪除紀錄') == (event.message.text):
        line_bot_api.reply_message(event.reply_token, buttons_template(today,user_id))

# 目前狀態: (呈現本周運動次數&日誌)
    elif '目前狀態'== event.message.text:
        range=7
        range,count,table,firstday,today=count_exercise(user_id, range)
        textmessage = f"{table}\n\n建議手機轉橫向查看表格(｡･ω･｡)"
        textmessage02=f"{firstday}至\t{today}間\n您本周運動{count}次(*'ω'*)\n以上為本周運動日誌"
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=textmessage),TextSendMessage(text=textmessage02)])

    elif '不用了' == event.message.text:
        pass


### 運動日誌=================================================================
    # 查詢紀錄 日期確認: database.usertable.checkdate(user_id)
    elif '對，確認查詢~' == event.message.text:
        startdate=checkdate(user_id)[1]
        enddate=checkdate(user_id)[2]
        table=search_exerciselog(user_id, startdate, enddate)
        textmessage=f" {startdate} 至  {enddate} 運動日誌:\n{table}\n建議手機轉橫向查看表格(｡･ω･｡)"

        text_quickreply0 = QuickReplyButton(action=MessageAction(label="更新紀錄", text="我要更新紀錄~"))
        text_quickreply1 = QuickReplyButton(action=MessageAction(label="刪除紀錄", text="我要刪除紀錄~"))
        text_quickreply2 = QuickReplyButton(action=MessageAction(label="不用了", text="不用了"))
        quick_reply_array = QuickReply(items=[text_quickreply0, text_quickreply1,text_quickreply2])
        reply_text_message = TextSendMessage(text=textmessage, quick_reply=quick_reply_array)
        line_bot_api.reply_message(event.reply_token, [reply_text_message])
        deletedate(user_id)
    elif '我要更新紀錄~'== event.message.text:
        textmessage="請複製格式，並輸入該筆紀錄的id & 內容~~"
        textmessage02="**範例**\n更新=99(請填入id)，內容：今天終於有時間運動惹~開心(*´∀`)♪(請填入日誌內容)"
        textmessage03 ="**格式**\n更新=，內容："
        text_quickreply0 = QuickReplyButton(action=MessageAction(label="重新查詢", text="查詢紀錄"))
        text_quickreply1 = QuickReplyButton(action=MessageAction(label="回主選單", text="回主選單"))
        quick_reply_array = QuickReply(items=[text_quickreply0, text_quickreply1])
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=textmessage02),TextSendMessage(text=textmessage03),TextSendMessage(text=textmessage,quick_reply=quick_reply_array)])

    elif '我要刪除紀錄~'== event.message.text:
        textmessage = "請複製格式，並輸入該筆紀錄的id~~"
        textmessage02 = "**範例**\n刪除=99(請填入id)"
        textmessage03 = "**格式**\n刪除="
        text_quickreply0 = QuickReplyButton(action=MessageAction(label="重新查詢", text="查詢紀錄"))
        text_quickreply1 = QuickReplyButton(action=MessageAction(label="回主選單", text="回主選單"))
        quick_reply_array = QuickReply(items=[text_quickreply0, text_quickreply1])
        line_bot_api.reply_message(event.reply_token,
                                   [TextSendMessage(text=textmessage02), TextSendMessage(text=textmessage03),
                                    TextSendMessage(text=textmessage, quick_reply=quick_reply_array)])

    elif '錯了，我想重新選擇日期~' == event.message.text:
        deletedate(user_id)
        textmessage = '請選擇運動日期~٩(๑❛ᴗ❛๑)۶' # \[TextSendMessage(text=textmessage)
        line_bot_api.reply_message(event.reply_token, buttons_template(today,user_id))


# 查詢紀錄-2 日期確認
## 更新 / 刪除紀錄-2
# 當使用者輸入
    elif "更新=" in msg_content:
        if "，內容：" in msg_content:
            sep = msg_content.split("，內容：")
            id = sep[0].split("=")[1]
            record=sep[1]
            print("將更新的id&record:",id,record)
            textmessage = f"準備更新id={id}\n==新的日誌內容==\n{record}"
            textmessage02 = updatelog(user_id,id,record)
            text_quickreply0 = QuickReplyButton(action=MessageAction(label="重新查詢", text="查詢紀錄"))
            text_quickreply1 = QuickReplyButton(action=MessageAction(label="回主選單", text="回主選單"))
            quick_reply_array = QuickReply(items=[text_quickreply0, text_quickreply1])
            line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=textmessage), TextSendMessage(text=textmessage02, quick_reply=quick_reply_array)])

        else:
            textmessage = f"格式錯誤Q^Q"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=textmessage))

    elif "刪除=" in msg_content:
        id = msg_content.split("=")[1]
        print("將刪除的id:", id)
        date,record=search_onelog(user_id, id)
        textmessage = f"準備刪除id={id}\n日期{date}\n=原有日誌內容=\n{record}"
        textmessage02=deletelog(user_id,id)
        text_quickreply0 = QuickReplyButton(action=MessageAction(label="重新查詢", text="查詢紀錄"))
        text_quickreply1 = QuickReplyButton(action=MessageAction(label="回主選單", text="回主選單"))
        quick_reply_array = QuickReply(items=[text_quickreply0, text_quickreply1])
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=textmessage),
                                                       TextSendMessage(text=textmessage02,
                                                                       quick_reply=quick_reply_array)])


    ####檢查目前state的日期是什麼，把內容存進相對應的欄位中。
    ## 新增紀錄-2 放最底下不要亂移動XDD
    # 當使用者輸入運動日誌(msg_content)
    # 從usertable-state抓回日期: database.usertable.checkstate
    # 從database.exercise.updatecheck(user_id, date)確認 exercise的record欄位是不是空的，避免重複寫入
    # 詢問使用者是否更新
    # 無日期:結束 / 有日期:確認是否存取(quickreply 是/否) =>Postback
    else:
        state = checkstate(user_id)
        if "checkstate=Y" in state:
            date = state.split(",")[1]
            last_record = updatecheck(user_id, date)
            if str(last_record) == "None":
                print("還未寫入record過，詢問是否新增")
                text_quickreply0 = QuickReplyButton(action=PostbackAction(label='是', display_text='是',
                                                                          data=f"update=Y,date={date},record={msg_content}"))
                text_quickreply1 = QuickReplyButton(action=PostbackAction(label='否', display_text='否', data='update=N'))
                # 有空新增第三個按鈕:重新選擇日期
                quick_reply_array = QuickReply(items=[text_quickreply0, text_quickreply1])
                reply_text_message = TextSendMessage(
                    f"{date}\n--------------------\n{msg_content}\n--------------------\n是否紀錄此筆日誌?",
                    quick_reply=quick_reply_array)
                line_bot_api.reply_message(event.reply_token, [reply_text_message])
            else:
                print("已經有日誌，詢問是否更新?")
                text_quickreply0 = QuickReplyButton(action=PostbackAction(label='是', display_text='是',
                                                                          data=f"update=Y,date={date},record={msg_content}"))
                text_quickreply1 = QuickReplyButton(action=PostbackAction(label='否', display_text='否', data='update=N'))
                # 有空新增第三個按鈕:重新選擇日期
                quick_reply_array = QuickReply(items=[text_quickreply0, text_quickreply1])
                reply_text_message = TextSendMessage(
                    f"原本已經有紀錄\n{date}\n--------------------\n{last_record}\n--------------------\n是否覆蓋並更新此筆日誌，如下?\n{date}\n--------------------\n{msg_content}\n--------------------\n ",
                    quick_reply=quick_reply_array)
                line_bot_api.reply_message(event.reply_token, [reply_text_message])

    return "message_event done"