import json
from linebot import (LineBotApi, WebhookHandler)

# with open('Line_access_token.txt', 'r', encoding='utf-8') as f:
#     token = json.load(f)
# line_bot_api = LineBotApi(token['Channel_access_token'])
# handler = WebhookHandler(token['Channel_secret'])
line_bot_api = LineBotApi("F14d3UkttcHnNw++sayJcqkvbHb71oY6uI0I9nGRrQqoqw+UWi6jUYx+wZTsuGg33lBmRg2to3K0AKv4v9MOODN4Or0M9G2iwFaqxOikXtyziecSxIIhpF3Es3M+IorvlOJRLIgDxva9vDYDRsD56gdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("51b155e535d838caf101446f96ce6bc9")

print("access_token讀取完成~")