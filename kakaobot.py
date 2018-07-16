# -*- coding: utf-8 -*-

import os
from flask import Flask,request,jsonify
import sys
import io
import urllib.parse as rep
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
from bs4 import BeautifulSoup

Mbase = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="
Mquote = rep.quote_plus("숭실대학교 미세먼지")
Murl= Mbase + Mquote

Wbase = "https://weather.naver.com/rgn/townWetr.nhn?naverRgnCd=09590102"


#################################system Setting################################

app = Flask(__name__)

@app.route('/keyboard')
def Keyboard():

    dataSend = {
            "message":{
                "text":"매일 아침 8시에 간략한 정보를 드리며,\n원하시는 경우에는 버튼을 눌러 서비스를 이용하세요\n BETA Version"
            },
        "type" : "buttons",
        "buttons" : ["현재 날씨", "오전 온도","오후 온도","내일 날씨","미세먼지"]
    }
    return jsonify(dataSend)


@app.route('/message',methods = ['POST'])
def Message():
    dataReceive = request.get_json()
    content = dataReceive['content']
    if content == u"현재 날씨":
        import urllib.request as req
        Wres = req.urlopen(Wbase).read()
        Wsoup = BeautifulSoup(Wres, "html.parser")

        now = Wsoup.select_one('div.w_now2 em')

        dataSend = {
            "message":{
                "text":now.text.strip()
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도","내일 날씨","미세먼지"]
            }
        }
    elif content ==u"오전 온도":
        import urllib.request as req
        Wres = req.urlopen(Wbase).read()
        Wsoup = BeautifulSoup(Wres, "html.parser")

        ATemp = Wsoup.select_one('table.tbl_weather ul.text')
        dataSend = {
            "message":{
                "text":ATemp.text
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도","내일 날씨","미세먼지"]
            }
        }
    elif content ==u"오후 온도":
        import urllib.request as req
        Wres = req.urlopen(Wbase).read()
        Wsoup = BeautifulSoup(Wres, "html.parser")

        BTemp = Wsoup.select_one('table.tbl_weather div:nth-of-type(2) ul.text ')
        dataSend = {
            "message":{
                "text":BTemp.text
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도","내일 날씨","미세먼지"]
            }
        }
    elif content ==u"내일 날씨":
        dataSend = {
            "message":{
                "text":"오전 혹은 오후를 클릭해주세요"
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["내일 오후","내일 오전","취소"]
            }
        }
    elif content ==u"내일 오후":
        import urllib.request as req
        Wres = req.urlopen(Wbase).read()
        Wsoup = BeautifulSoup(Wres, "html.parser")

        TBTemp = Wsoup.select_one('table.tbl_weather td:nth-of-type(2) div:nth-of-type(2) ul.text ')
        dataSend = {
            "message":{
                "text":TBTemp.text
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도","내일 날씨","미세먼지"]
            }
        }
    elif content ==u"내일 오전":
        import urllib.request as req
        Wres = req.urlopen(Wbase).read()
        Wsoup = BeautifulSoup(Wres, "html.parser")

        TBTemp = Wsoup.select_one('table.tbl_weather td:nth-of-type(2) div:nth-of-type(1) ul.text ')
        dataSend = {
            "message":{
                "text":TBTemp.text
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도","내일 날씨","미세먼지"]
            }
        }
    elif content ==u"미세먼지":
        dataSend = {
            "message":{
                "text":"원하시는 기능을 선택해 주세요\n0-30 > 좋음\n30-80 > 보통\n80-150 > 나쁨\n 그 이상 > 매우 나쁨"
            },
            "keyboard":{
                "type":"buttons",
                "buttons":['현재 미세먼지','24시간 평균','초미세먼지',"취소"]
            }
        }
    elif content ==u"현재 미세먼지":
        import urllib.request as req
        Mres = req.urlopen(Murl).read()
        Msoup = BeautifulSoup(Mres, "html.parser")
        NowmicroDust = Msoup.select('div.air_detail span.figure')

        dataSend = {
            "message":{
                "text":NowmicroDust[0].text
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도","내일 날씨","미세먼지"]
            }
        }
    elif content ==u"24시간 평균":
        import urllib.request as req
        Mres = req.urlopen(Murl).read()
        Msoup = BeautifulSoup(Mres, "html.parser")
        AlldaymicroDust = Msoup.select('div.air_detail span.figure')

        dataSend = {
            "message":{
                "text":AlldaymicroDust[1].text
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도","내일 날씨","미세먼지"]
            }
        }
    elif content ==u"초미세먼지":
        import urllib.request as req
        Mres = req.urlopen(Murl).read()
        Msoup = BeautifulSoup(Mres, "html.parser")
        nanoDust = Msoup.select_one('div.all_state span.state_info')

        dataSend = {
            "message":{
                "text":nanoDust.text
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도","내일 날씨","미세먼지"]
            }
        }
    elif content ==u"취소":
        dataSend = {
            "message":{
                "text":"메인메뉴로 갑니다"
            },
            "keyboard":{
                "type":"buttons",
                "buttons":["현재 날씨", "오전 온도","오후 온도","내일 날씨","미세먼지"]
            }
        }
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 6000)
