import os

import requests
import json

from django.shortcuts import render
from django.http import HttpResponse
from .tools.parser import Concierge

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'

HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
}


def index(request):
    return HttpResponse('Top page')


def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
    return HttpResponse(reply)  # テスト用


def reply_text(reply_token, text):
    concierge = Concierge()
    res = concierge.talk()

    payload = {
          "replyToken": reply_token,
          "messages": [
                {
                    "type": "text",
                    "text": res
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return 'test'

