from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from engine.currencysearch import currencysearch
from engine.AQI import AQImonitor
from engine.gamma import gammamonitor
from engine.OWM import OWMLonLatsearch

app = Flask(__name__)

# 設定你的Channel Access Token
line_bot_api = LineBotApi('O7EffG4zswadhgFJzRGyDnWMQ/DUzyB6qiuai3OrUvZD/NTb+wNK3AwO1C41VNToQbIYCBLziMPxKArEZwuRitu/j5fhqiUC7sKuVk/5dhWUWZuN1Gjp5E9cVCwb5SVw+j8pPy+3Ooi6Hkg2NmQiCQdB04t89/1O/w1cDnyilFU=')
# 設定你的Channel Secret
handler = WebhookHandler('c4cd9b284cf6bd3f633f2f40d2ff4b32')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

@app.route("/web")
def shoeweb():
    return '<h1>Hello Every one</h1>'

#處理訊息
#當訊息種類為TextMessage時，從event中取出訊息內容，藉由TextSendMessage()包裝成符合格式的物件，並貼上message的標籤方便之後取用。
#接著透過LineBotApi物件中reply_message()方法，回傳相同的訊息內容
#@handler.add(MessageEvent, message=TextMessage)
#def handle_message(event):
    #coin = twder.now(currency) 
    #message = TextSendMessage(text=coin)
    #line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userSend = event.message.text
    userid = event.source.user_id
    if userSend == '白癡':
        message = TextSendMessage(text='!!!!不要自我介紹'+userid)
    elif userSend == '你好':
        message = TextSendMessage(text='你好'+userid)
    elif userSend == '再見':
        #line_bot_api.push_message()
        message = TextSendMessage(package_id='11537',sticker_id='52002758')
    elif userSend == '美金':
        #dollarTuple = twder.now('USD')
        #reply = '{}\n美金的即期賣出價:{}'.format(dollarTuple[0],dollarTuple[4])
        message = TextSendMessage(text = currencysearch('USD'))
    elif userSend == '日圓':
        message = TextSendMessage(text = currencysearch('JPY'))
    elif userSend in ['CNY', 'THB', 'SEK', 'USD', 'IDR', 'AUD', 'NZD', 'PHP', 'MYR', 'GBP', 'ZAR', 'CHF', 'VND', 'EUR', 'KRW', 'SGD', 'JPY', 'CAD', 'HKD']:
        message = TextSendMessage(text = currencysearch(userSend))
    else:
        message = TextSendMessage(text=userSend+userid)
    line_bot_api.reply_message(event.reply_token, message)
@handler.add(MessageEvent, message=LocationMessage)
def handle_message(event):
    useradderss = event.message.address
    userlat = event.messade_latitude
    userlon = event.message_longitude
    weatherresult = OWMLonLatsearch(userlon, userlat)
    AQIresult = AQImonitor(userlon, userlat)

    message = TextSendMessage(text='天氣狀況:\n{}\n空氣品質:\n{}\n輻射值:{}\n'.format(weatherresult,AQIresult,gammamonitor))
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)
@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
    message = TextSendMessage(text='白癡')
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

