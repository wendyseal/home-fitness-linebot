from linebot.models import (PostbackAction,QuickReply, QuickReplyButton, TextSendMessage)
from config import line_bot_api
from database.usertable import savebasic01

def handle(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    print(profile)
    print(type(profile))
    # 開啟檔案，將用戶個資1.display_name 2.user_id 3.picture_url，存入DB
    # display_name = user_profile['displayName']
    # user_id=user_profile['userId']
    # picture_url = user_profile['pictureUrl']
    # 建立文字消息
    follow_text_send_message = TextSendMessage(str(profile.display_name)+"你好～我是教練Seal，歡迎歡迎！\n一起來動滋動吧！\n為了幫你量身打造適合的運動，先讓我對你有更多認識吧(❁´◡`❁)")
    # 創造一個QuickReplyButton
    text_quickreply0 = QuickReplyButton(action=PostbackAction(label='男', display_text='我是男生~',data='gender=male'))
    text_quickreply1 = QuickReplyButton(action=PostbackAction(label='女', display_text='我是女生~',data='gender=female'))
    text_quickreply2 = QuickReplyButton(action=PostbackAction(label='其他', display_text='我想選擇其他',data='gender=other'))
    # 創造一個QuickReply，並把剛剛創建的button放進去
    quick_reply_array1 = QuickReply(items=[text_quickreply0, text_quickreply1, text_quickreply2])

    # 生成一個文字消息
    reply_text_message1= TextSendMessage('性別是?', quick_reply=quick_reply_array1)
    line_bot_api.reply_message(event.reply_token, [follow_text_send_message, reply_text_message1])

    #儲存使用者資料
    print(user_id,profile.display_name,profile.picture_url)
    savebasic01(user_id, profile.display_name, profile.picture_url)
    return "FollowEvent done"
