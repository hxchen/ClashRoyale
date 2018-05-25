import urllib.request
from bs4 import BeautifulSoup
import json
import uuid
import pymysql
import time
import ssl
from configparser import ConfigParser
# 读取配置信息
cfg = ConfigParser()
cfg.read('config.ini')

ssl._create_default_https_context = ssl._create_unverified_context

#   服务器 false ;本地 true
debug_model = False
# debug_model = True

if(debug_model):
    db_host = cfg.get('test_db','db_host')
    db_user = cfg.get('test_db','db_user')
    db_password = cfg.get('test_db','db_password')
    db_name = cfg.get('test_db','db_name')

else:
    db_host = cfg.get('pro_db','db_host')
    db_user = cfg.get('pro_db','db_user')
    db_password = cfg.get('pro_db','db_password')
    db_name = cfg.get('pro_db','db_name')

# 请求头信息参数设置
clan_url = "https://statsroyale.com/clan/8RCCQC/war"
clan_refresh_url = "https://statsroyale.com/clan/8RCCQC/refresh"

cookie = "__cfduid=d625ab65edd3bdb904548d64e6c06fbe21493566873; XSRF-TOKEN=eyJpdiI6InlKWXkyQTFpdUpPTjlcL294S3dzNjJnPT0iLCJ2YWx1ZSI6InJCS1dIVzJkTG1Dbzk2eWxYRWRKZVpCZjdzVndXNEtWdUtpalVZaSswaW1uVG43Nk51bVwvR0hRK0pVanlPVmc2eGo1YjZVbXJLZnBcL1hhNFZJcFltNXc9PSIsIm1hYyI6Ijk2ZGViZDc1ZDg3MmU1YTIzMzYxYmVkYzFhY2NmOTZkMmU5ODI1ZjFkYmYzYWQ2NDZhODhhMTBhM2I5NDk4ZjgifQ%3D%3D; laravel_session=eyJpdiI6Ino0bWRNZGVTSXdXOWZRcnh6aU5Ob0E9PSIsInZhbHVlIjoidjJ5aVkyT1ZDVjg5bFhHMlQ2cmdjTVhWV2xkY2grUG96dEZnaXRtdGhpYmo1SlwvSENXNTVvMmZDRndReExON3l0TWJoZmxqQWdLbk4xdDZpMTdBbnNRPT0iLCJtYWMiOiJlNjBiMTEyMzE4NzE3Nzc3NzJiZDhiYjAwYTlmNjE2MjI2YzUxYmNlMzgxODI0ZTJhOTc1ODhiNWQ4NWFlYzdjIn0%3D"
Host = "statsroyale.com"
Connection = "keep-alive"
Pragma = "no-cache"
CacheControl = "no-cache"
UpgradeInsecureRequests = "1"
UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
Accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
AcceptLanguage = "zh-CN,zh;q=0.8,tr;q=0.6,en;q=0.4,zh-TW;q=0.2,sq;q=0.2,ja;q=0.2"

def get_header(url):
    req = urllib.request.Request(url)
    req.add_header("cookie", cookie)
    req.add_header("Host", Host)
    req.add_header("Connection", Connection)
    req.add_header("Pragma", Pragma)
    req.add_header("Cache-Control", CacheControl)
    req.add_header("Upgrade-Insecure-Requests", UpgradeInsecureRequests)
    req.add_header("User-Agent", UserAgent)
    req.add_header("Accept", Accept)
    req.add_header("Accept-Language", AcceptLanguage)
    return req

"""
刷新部落信息页面
"""


def refresh_clan():
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("refresh clan data at "+start_time)
    req = get_header(clan_refresh_url)
    response = urllib.request.urlopen(req).read().decode("utf-8")
    content = json.loads(response)
    print(content['message'])


"""
获取部落战数据
"""
def get_war():
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("fetch war data start at "+start_time)
    req = get_header(clan_url)
    response = urllib.request.urlopen(req).read().decode("utf-8")
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("fetch war data end at "+end_time)
    soup = BeautifulSoup(response,"html.parser")
    for i, row in enumerate(soup.findAll("div",attrs = {"class":"clanParticipants__rowContainer"})):
        user_dict = {}
        for j,col in enumerate(row.findAll("div",attrs = {"class":"clanParticipants__row"})):
            if j == 0:
                user_dict["rank"] = col.string.strip().replace("#","")
            elif j == 1:
                user_dict["name"] = col.a.string.strip()
                link = col.a.get("href")
                uid = link.replace("https://statsroyale.com/profile/","")
                user_dict["uid"] = uid
            elif j == 2:
                user_dict["battles"] = col.get_text()
            elif j == 3:
                user_dict["wins"] = col.get_text()
            elif j == 4:
                user_dict["clan_cards"] = col.get_text()
        print(user_dict)


def main():
    get_war()


main()