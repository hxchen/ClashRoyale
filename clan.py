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
# debug_model = False
debug_model = True

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
clan_url = "https://statsroyale.com/clan/8RCCQC"
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

#   所有成员uid-profile信息
profile_list_all = {}


def rank(value):
    return value.string.strip()


def name(value):
    return value.a.string


def level(value):
    return value.div.span.string


def league(value):
    if value.img is not None:
        return value.img.get('src')
    else:
        return ""


def score(value):
    return value.string.strip()


def donations(value):
    return value.string.strip()


def role(value):
    return value.get_text().strip()


def extra(value):
    return None


category = {
    0:rank,
    1:name,
    2:level,
    3:league,
    4:score,
    5:donations,
    6:role,
    7:extra
}


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
获取部落成员数据,入库
"""
#


def get_clan2():
    profile_list = []

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("get_clan2 fetch data start at "+start_time)
    req = get_header(clan_url)
    response = urllib.request.urlopen(req).read().decode("utf-8")
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("get_clan2 fetch data end at "+end_time)
    soup = BeautifulSoup(response,"html.parser")

    pid = uuid.uuid1()
    this_week = time.strftime("%W")
    this_year = time.strftime("%Y")
    db = pymysql.connect(db_host,db_user,db_password,db_name,charset="utf8")
    cursor = db.cursor()
    for i, row in enumerate(soup.findAll("div",attrs = {"class":"clan__rowContainer"})):
        user_dict = {}
        for j,col in enumerate(row.findAll("div",attrs = {"class":"clan__row"})):
            if j == 0:
                user_dict["rank"] = col.string.strip().replace("#","")
            elif j == 1:
                user_dict["name"] = col.a.string.strip()
                link = col.a.get("href")
                uid = link.replace("https://statsroyale.com/profile/","")
                user_dict["uid"] = uid
                profile_list.append(uid)
            elif j == 2:
                user_dict["level"] = col.span.string.strip()
            elif j == 3:
                user_dict["league"] = col.contents[1].div.get("class")[0].replace("league__","")
            elif j == 4:
                user_dict["score"] = col.div.string.strip()
            elif j == 5:
                user_dict["donations"] = col.div.string.strip()
            elif j == 6:
                user_dict["role"] = col.string.strip()
        if user_dict:
            # print(user_dict)
            try:
                sql = "INSERT INTO cr_clan_8RCCQC(pid, rank, uid, name, level, league, score, donations, role, updateTime,year,week) VALUES ('"+str(pid)+"','"+user_dict["rank"]+"','"+user_dict["uid"]+"','"+user_dict["name"]+"','"+user_dict["level"]+"','"+user_dict["league"]+"',"+user_dict["score"]+","+user_dict["donations"]+",'"+user_dict["role"]+"','"+end_time+"',"+this_year+","+this_week+")"
                # print(sql)
                cursor.execute(sql)
            except Exception as e:
                print(e)
            profile_list_all[uid] = user_dict
    try:
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()

    # print(profile_list)
    # print(profile_list_all)

    for profile_id in profile_list:
        print("-----------------------"+profile_id+"-----------------------")
        refresh_profile(profile_id)
        # refresh_battles(profile_id)

    time.sleep(60)

    for profile_id_twice in profile_list:
        analytics_profile(profile_id_twice,1)

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


def refresh_profile(id):
    profile_url = "https://statsroyale.com/profile/"+id+"/refresh"
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("refresh refresh_profile data of "+profile_list_all[id]["name"]+" at "+start_time)
    req = get_header(profile_url)
    response = urllib.request.urlopen(req).read().decode("utf-8")
    content = json.loads(response)
    print(content['message'])


def refresh_battles(id):
    battles_url = "https://statsroyale.com/battles/"+id+"/refresh"
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("refresh refresh_battles data of "+profile_list_all[id]["name"]+" at "+start_time)
    req = get_header(battles_url)
    response = urllib.request.urlopen(req).read().decode("utf-8")
    content = json.loads(response)
    print(content['message'])


def analytics_profile(id,has_info):
    profile_url = "https://statsroyale.com/profile/"+id
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    this_week = time.strftime("%W")
    this_year = time.strftime("%Y")

    if has_info:
        print("fetch "+profile_list_all[id]["name"]+" data start at "+start_time)
    else:
        print("fetch "+id+" data start at "+start_time)
    req = get_header(profile_url)
    try:
        # 添加超时处理
        response = urllib.request.urlopen(req,timeout=10).read().decode("utf-8")
    except Exception as e:
        print("timeout")
        print(e)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        response = urllib.request.urlopen(req,timeout = 15).read().decode("utf-8")
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    print("fetch "+id+" data end at "+end_time)
    soup = BeautifulSoup(response,"html.parser")
    profile_list = {}
    profile_list["id"] = id

    for value in soup.find_all("span",{"class":"profileHeader__nameCaption"}):
        name = value.get_text().strip()
        profile_list["name"] = name
    for value in soup.find_all("span",{"class":"profileHeader__userLevel"}):
        level = value.get_text()
        profile_list["level"] = level
    for value in soup.find_all("a",{"class":"ui__link ui__mediumText profileHeader__userClan"}):
        clan = value.get_text().strip()
        profile_list["clan"] = clan
    # TROPHIES
    # print("*******************TROPHIES*******************")
    trophies = soup.find_all(attrs={"class": "statistics__subheader statistics__trophyCaption"})
    next_siblings = trophies[0].find_next_siblings(limit=2)
    for value in next_siblings:
        description = value.contents[1].get_text().lower().replace(" ","_")
        content = value.contents[5].get_text()
        # print(description+", " + content)
        profile_list[description] = content

    # STATS ROYALE
    # print("*******************STATS ROYALE*******************")
    trophies = soup.find_all(attrs={"class": "statistics__subheader statistics__matchesCaption"})
    next_siblings = trophies[0].find_next_siblings(limit=4)
    for value in next_siblings:
        description = value.contents[1].get_text().lower().replace(" ","_")
        content = value.contents[5].get_text()
        # print(description+", " + content)
        profile_list[description] = content

    # CLAN WAR STATS
    # print("*******************CLAN WAR STATS*******************")
    trophies = soup.find_all(attrs={"class": "statistics__subheader statistics__clanwarCaption"})
    next_siblings = trophies[0].find_next_siblings(limit=2)
    for value in next_siblings:
        description = value.contents[1].get_text().lower().replace(" ","_")
        content = value.contents[5].get_text()
        print(description+", " + content)
        profile_list[description] = content

    # TOURNAMENT STATS
    # print("*******************TOURNAMENT STATS*******************")
    challenge_stats = soup.find_all(attrs={"class": "statistics__subheader statistics__tournamentCaption"})
    next_siblings = challenge_stats[0].find_next_siblings(limit=4)
    for value in next_siblings:
        description = "tournament_"+value.contents[1].get_text().lower().replace(" ","_").replace("-","_")
        content = value.contents[5].get_text()
        # print(description+", " + content)
        profile_list[description] = content

    # CHALLENGE STATS
    # print("*******************CHALLENGE STATS*******************")
    challenge_stats = soup.find_all(attrs={"class": "statistics__subheader statistics__challengeCaption"})
    next_siblings = challenge_stats[0].find_next_siblings(limit=2)
    for value in next_siblings:
        description = "challenge_"+value.contents[1].get_text().lower().replace(" ","_")
        content = value.contents[5].get_text()
        # print(description+", " + content)
        profile_list[description] = content

    # PREVIOUS SEASON
    # print("*******************PREVIOUS SEASON*******************")
    previous_season = soup.find_all(attrs={"class": "statistics__subheader statistics__seasonCaption"})
    next_siblings = previous_season[0].find_next_siblings(limit=3)
    for value in next_siblings:
        description = "prev_season_"+value.contents[1].get_text().lower().replace(" ","_")
        content = value.contents[5].get_text()
        # print(description+", " + content)
        profile_list[description] = content

    # BEST SEASON
    # print("*******************CHALLENGE STATS*******************")
    best_season = soup.find_all(attrs={"class": "statistics__subheader statistics__bestCaption"})
    next_siblings = best_season[0].find_next_siblings(limit=3)
    for value in next_siblings:
        description = "best_season_"+value.contents[1].get_text().lower().replace(" ","_")
        content = value.contents[5].get_text()
        # print(description+", " + content)
        profile_list[description] = content

    # LEAGUE SEASON
    # print("*******************LEAGUE SEASON*******************")
    league_season = soup.find_all("div", {"class" : lambda L: L and L.startswith('statistics__subheader statistics__league-')})
    next_siblings = league_season[0].find_next_siblings(limit=1)
    for value in next_siblings:
        description = "league_season_"+value.contents[1].get_text().lower().replace(" ","_")
        content = value.contents[5].get_text()
        # print(description+", " + content)
        profile_list[description] = content


    profile_list["update_time"] = end_time
    profile_list["year"] = this_year
    profile_list["week"] = this_week

    # print(profile_list)
    db = pymysql.connect(db_host,db_user,db_password,db_name,charset="utf8")

    cursor = db.cursor()
    try:
        placeholders = ', '.join(['%s'] * len(profile_list))
        columns = ', '.join(profile_list.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('cr_profile', columns, placeholders)
        # print(sql)
        cursor.execute(sql, list(profile_list.values()))
        db.commit()
    except Exception as e:
        print(e)
    finally:
        db.close()


def get_battles():
    print("fetch battles")


def get_data_by_uids():
    profile_list = ['2LQYLYJQ', '9U8QLY9V', '2P0V2CCY', '9PLUY020', '20PGL82J8', '20RRU0LJ2', 'Q0R0YQVC', '8RLQJQRR', 'U2R2LGR2', '8Q2J8LVP', 'LCP9CL8C', 'PL9VU80U', 'U22L0GGQ', 'QQUV9RR9', '2L9UPJP0', '9YC2LUPR', 'UG8JCJ8C', 'QY2Y9R0J', 'GPGLJ0C', '92Q29R0U', 'QGVYJCYG', '22GUQYV8Y', 'UPPGLURG', '2L29R2V8', 'JUGJ88GP', '80GUU0U2', 'Y8CJQGVR', 'J9UPRG29', '8VCLUVLY', '8890PLQV', '2PLQQLPC', '822CJCU0G', '28JR0VPP9', '2JRCC2LY9', '2229LG9PG', '2JGJYG8UQ', '20QJRYC2Q', '2RVPUG2P', '82UPP8PPR', 'UJQP9LG9', '2Y2P9QC9L', '2JJ9G00JR']
    for profile_id_twice in profile_list:
        analytics_profile(profile_id_twice,0)


def main():
    refresh_clan()
    time.sleep(15)
    get_clan2()
    # refresh_profile("99220PPR8")
    # refresh_battles("2P0V2CCY")
    # analytics_profile("2LQYLYJQ",0)
    # get_data_by_uids()
main()







