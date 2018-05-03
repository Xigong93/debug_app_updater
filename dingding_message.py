# encoding=utf-8
import requests

__author__ = 'pokercc'
"""钉钉消息机器人"""
ACCESS_TOKEN = ''
DINGDING_URL = f'https://oapi.dingtalk.com/robot/send?access_token={ACCESS_TOKEN}'


def send_message(content):
    assert content
    data = {"msgtype": "text", "text": {"content": content}}
    res = requests.post(DINGDING_URL, json=data, timeout=(3, 60))
    res.raise_for_status()
    assert res.json().get('errcode') == 0, f'发送失败,{res.json()}'
    print(f'发送成功,{res.json()}')


if __name__ == '__main__':
    send_message("今天中午吃什么?请点击https://www.zwcsm.com/")
