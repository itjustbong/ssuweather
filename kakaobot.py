# -*- coding: utf-8 -*-

import os
from flask import Flask,request,jsonify
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

#######

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument('--headless')#cli

weather = webdriver.Chrome(chrome_options = chrome_options, executable_path ='E:\WorkSpace\section3\webdriver\chrome\chromedriver')
weather.implicitly_wait(1)
#################################system Setting################################

app = Flask(__name__)

@app.route('/keyboard')
def Keyboard():

    dataSend = {
        "type" : "buttons",
        "buttons" : ["현재 날씨", "오전 온도","오후 온도"]
    }
    return jsonify(dataSend)


@app.route('/message',methods = ['POST'])
def Message():
    dataReceive = request.get_json()
    content = dataReceive['content']
    if content == u"현재 날씨":
        weather.get("https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=09590102")
        weather.implicitly_wait(1)

        #################네이버 날씨에서 동작구 날씨 가져오기################
        now = weather.find_element_by_css_selector('#content > div.w_now2 > ul > li:nth-child(1) > div > em')  #

        dataSend = {
            "message":{
                "text":now.text
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도"]
            }
        }
    elif content ==u"오전 온도":
        weather.get("https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=09590102")
        weather.implicitly_wait(1)
        #################네이버 날씨에서 동작구 날씨 가져오기################
        TATemp = weather.find_element_by_css_selector('#content > table.tbl_weather.tbl_today3 > tbody > tr > td:nth-child(1) > div:nth-child(1) > ul > li.nm')#오전 강수량

        dataSend = {
            "message":{
                "text":TATemp.text
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도"]
            }
        }
    elif content ==u"오후 온도":
        weather.get("https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=09590102")
        weather.implicitly_wait(1)
        #################네이버 날씨에서 동작구 날씨 가져오기################
        TBTemp = weather.find_element_by_css_selector('#content > table.tbl_weather.tbl_today3 > tbody > tr > td:nth-child(1) > div:nth-child(3) > ul > li.nm ')#오전 날씨

        dataSend = {
            "message":{
                "text":TBTemp.text
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도"]
            }
        }
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 6000)
