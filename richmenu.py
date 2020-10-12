from linebot import (LineBotApi)
from linebot.models import (RichMenu)
import json
import requests
#主選單
#richmenu-6751b6c408e76782f9abedf0625c894e
#richmenu02
#richmenu-01b7846ff426cbce7096eb905589aab4
line_bot_api = LineBotApi("F14d3UkttcHnNw++sayJcqkvbHb71oY6uI0I9nGRrQqoqw+UWi6jUYx+wZTsuGg33lBmRg2to3K0AKv4v9MOODN4Or0M9G2iwFaqxOikXtyziecSxIIhpF3Es3M+IorvlOJRLIgDxva9vDYDRsD56gdB04t89/1O/w1cDnyilFU=")
# 1. 拿設定擋去申請圖文選單：讀取json檔 轉成json格式 將json格式做成RichMenu的變數 line_bot_api傳給line 把rich_menu_id打印出來
# with open('richmenu/richmenu02.json', 'r', encoding='utf8') as json_file:
#     rich_menu_json_object=json.load(json_file)
# rich_menu_config=RichMenu.new_from_json_dict(rich_menu_json_object)
# rich_menu_id=line_bot_api.create_rich_menu(rich_menu_config)
# print(rich_menu_id)

# #2.把照片傳給指定的圖文選單id： 把圖片載入 命令line_bot_api 將圖片上傳到指定圖文傳單的id上
# rich_menu_id='richmenu-01b7846ff426cbce7096eb905589aab4'
# with open('richmenu/richmenu.png','rb') as image_file:
#     response=line_bot_api.set_rich_menu_image(
#         rich_menu_id=rich_menu_id,
#         content_type="image/png",
#         content=image_file )
# print(response)
# 3.綁定用戶與圖文選單
# line_bot_api.link_rich_menu_to_user(
#     user_id='Ua08a63ef695ab19d338ed8f9af60ca55',
#     rich_menu_id=rich_menu_id
# )
# #
# # # #4.解除綁定
# # line_bot_api.unlink_rich_menu_from_user(
# #     user_id='Ua08a63ef695ab19d338ed8f9af60ca55'
# # )
# # #
# # # #5.刪除圖文選單
# # # rich_menu_id='richmenu-6b926b832fff53a53c9177fec0638271'
# # # line_bot_api.delete_rich_menu(rich_menu_id=rich_menu_id)
# #
# #
#



































