from datetime import timedelta
from datetime import date
from linebot.models import (PostbackAction, PostbackTemplateAction,DatetimePickerAction, FlexSendMessage,
                            ImageCarouselTemplate,ImageCarouselColumn, TextSendMessage,
                            TemplateSendMessage,ButtonsTemplate, QuickReplyButton, QuickReply)
from database.usertable import checkdate
# from linebot.models.actions import PostbackAction, DatetimePickerAction

# def datechoose(today):
#     print("讀取function中")
#     ImageCarousel_Template=ImageCarouselTemplate(
#         columns=[ImageCarouselColumn(
#                     imageUrl='https://live.staticflickr.com/65535/50427588473_8586d26f5c_m.jpg',
#                     action=DatetimePickerAction(
#                         label="起始日期",
#                         data="startdate",
#                         mode="date",
#                         initial=today.strftime("%Y-%m-%d"),
#                         max=today.strftime("%Y-%m-%d"),
#                         min=(today - timedelta(days=2650)).strftime("%Y-%m-%d")
#                     ))])
#     # action = DatetimePickerAction(
#     #     label='選擇日期',
#     #     data='q1',  # action=buy&itemid=1
#     #     mode='date',
#     #     initial=today.strftime("%Y-%m-%d"),
#     #     min=(today - timedelta(days=30)).strftime("%Y-%m-%d"),
#     #     max=(today + timedelta(days=30)).strftime("%Y-%m-%d")
#     print("讀取function中-2")
#     image_carousel_template_message = TemplateSendMessage(alt_text='ImageCarousel template',
#                                                           template=ImageCarousel_Template)
#     print("讀取function中-3")
#     return  image_carousel_template_message


#新增紀錄
def buttons_templatenewdate(today):
    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://live.staticflickr.com/65535/50436378452_f0b97f86db_w.jpg',
            title='新增運動日誌',
            text='請選擇日期~٩(๑❛ᴗ❛๑)۶\n讀取日期需要一點時間，請稍後~',
            actions=[
                DatetimePickerAction(
                    label="運動日期",
                    data="q1",
                    mode="date",
                    initial=today.strftime("%Y-%m-%d"),
                    max=today.strftime("%Y-%m-%d"),
                    min=(today - timedelta(days=2650)).strftime("%Y-%m-%d")
                )]
        )
    )
    return  buttons_template_message

#查詢日誌-選擇日期=>Postback
def buttons_template(today,user_id):
    #
    # if 'search=Noall'==check[0]:
    #     changeday=today.strftime("%Y-%m-%d")
    # elif "search=Nostart"==check[0]:
    #     changeday=today.strftime("%Y-%m-%d")
    # elif "search=Noend"==check[0]:
    #     changeday=check[2]
    # print("changeday",changeday)
    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://live.staticflickr.com/65535/50435491973_816cca9757_c.jpg',
            title='查詢運動日誌',
            text='請選擇起始&結束日期~٩(๑❛ᴗ❛๑)۶\n查詢需要一點時間，請稍後~',
            actions=[
                DatetimePickerAction(
                    label="起始日期",
                    data="startdate",
                    mode="date",
                    initial=today.strftime("%Y-%m-%d"),
                    max=today.strftime("%Y-%m-%d"),
                    min=(today - timedelta(days=2650)).strftime("%Y-%m-%d")
                ),
                DatetimePickerAction(
                    label= "結束日期",
                    data= "enddate",
                    mode= "date",
                    initial=today.strftime("%Y-%m-%d"),
                    max=today.strftime("%Y-%m-%d"),
                    min=(today - timedelta(days=2650)).strftime("%Y-%m-%d"))
                ]
        )
    )
    return  buttons_template_message