from flask import Flask, request, abort
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage,  TextSendMessage,FollowEvent, PostbackEvent)
from datetime import datetime
from config import handler,line_bot_api
from controller import follow, message, postback
import os

app = Flask(__name__)

@app.route("/", methods=['GET'])
def connect():
    print ("success")
    return "success"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(controller):
#     line_bot_api.reply_message(
#         controller.reply_token,
#         TextSendMessage(text=controller.message.text))

@handler.add(MessageEvent, message=TextMessage )
def handle_message(event):
    message.handle(event)

@handler.add(FollowEvent)
def handle_follow(event):
    follow.handle(event)

@handler.add(PostbackEvent)
def handle_post(event):
    postback.handle(event)

# if __name__ == '__main__':
#     app.run()
#
# heroku專用，偵測heroku給我們的port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])