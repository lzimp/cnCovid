

import requests, random, re
import urllib.request
import numpy as np
import time
from bs4 import BeautifulSoup
from datetime import datetime as dt


def loadCovidList():
    user_agents = ["Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"]
    random_user_agent = random.choice(user_agents)
    headers = {'User-Agent': random_user_agent}
    url = 'http://www.nhc.gov.cn/yjb/s7860/new_list.shtml'
    #response = requests.get(url, headers=headers)
    #print(response)
    #soup = BeautifulSoup(response.text, features="lxml")
    #print(soup)
    #data = soup.find_all("li")
    #print(len(data), data)

    listName = "daily_covid19_list.txt"
    #cvfile = open(listName, "r")
    #cvlist = cvfile.read()#.split("\n")
    #print(cvlist, len(cvlist))
    with open(listName) as fl:
        lines = fl.read().splitlines()

    #print(lines)
    url = "http://www.nhc.gov.cn/"

    cvlist = []
    for line in lines:
        cvlist.append(url+line)

    #print(cvlist, len(cvlist))

    return cvlist

def loadCovidData():

    user_agents = ["Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"]
    random_user_agent = random.choice(user_agents)
    headers = {'User-Agent': random_user_agent}
    #print(headers)
    #url = 'http://www.nhc.gov.cn/yjb/s7860/202208/7bcb5ceeefe540ebb9289c37cc0afc41.shtml'
    #url = 'http://www.nhc.gov.cn/yjb/s7860/202208/e12653e6071944c4b5da52b7bd552f20.shtml' 
    #url = 'http://www.nhc.gov.cn/yjb/s7860/202208/8fbbe614bd0c4a5ca9cf8a9e4c289e9a.shtml'

    cvlist = loadCovidList()

    url = cvlist[-1]
    print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    print(soup)

    # get all the paragraphes in the page 
    data = soup.find_all("p")
    #print(data)
    print(len(data))

    for ip in range(7):
        print("第 %d 段内容： "%(ip+1), data[ip].get_text())

def skimData():

    rawdata = "9月3日0-24时，31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例384例。其中境外输入病例70例（广东18例，福建12例，上海9例，北京6例，内蒙古4例，黑龙江4例，四川4例，陕西4例，天津3例，河南2例，云南2例，辽宁1例，山东1例），含6例由无症状感染者转为确诊病例（四川2例，陕西2例，山东1例，广东1例）；本土病例314例（四川98例，广东79例，西藏51例，海南24例，辽宁11例，吉林11例，内蒙古10例，青海8例，黑龙江4例，天津3例，贵州3例，河北2例，浙江2例，江西2例，北京1例，上海1例，山东1例，湖南1例，重庆1例，陕西1例），含40例由无症状感染者转为确诊病例（海南16例，四川7例，西藏6例，吉林4例，青海4例，北京1例，黑龙江1例，浙江1例）。无新增死亡病例。无新增疑似病例。"

    lclProv = []
    rawsplt = re.split('。|；', rawdata)
    for s in rawsplt:
        if '本土病例' in s:
            lclProv.append(s)
        else:
            pass


    prvList = []
    prvsplt = re.split('（|），', lclProv[0])
    for lcl in prvsplt:
        prvList.append(lcl)

    # List for the context in the first paragraph: 每日新增确诊病例书、无症状转确诊病例数，
    # 及其分省信息。
    # 0: 全国总日增本土病例，    
    #print(prvList)
    ttlCase = int(re.sub(u"([^\u0030-\u0039])", "", prvList[0]))
    print(ttlCase, type(ttlCase))

    # 1: 本土分省日增病例，
    prvName, prvCase = [], []
    cassplt = re.split('，', prvList[1])
    for prv in cassplt:
        prvnm = re.sub(u"([^\u4e00-\u9fa5])", "", prv)
        prvName.append(prvnm[0:-1])
        prvCase.append(int(re.sub(u"([^\u0030-\u0039])", "", prv)))

    print(prvName, prvCase)

    # 2: 全国无症状转确诊病例数，3: 分省信息
    ttlAtcf = int(re.sub(u"([^\u0030-\u0039])", "", prvList[2]))
    atcName, atcCase = [], []
    atcsplt = re.split('，', prvList[3])
    for prv in atcsplt:
        atcnm = re.sub(u"([^\u4e00-\u9fa5])", "", prv)
        atcName.append(atcnm[0:-1])
        atcCase.append(int(re.sub(u"([^\u0030-\u0039])", "", prv)))

    print(atcName, atcCase)

    rawAsym = "31个省（自治区、直辖市）和新疆生产建设兵团报告新增无症状感染者1464例，其中境外输入105例，本土1359例（西藏505例，青海131例，辽宁113例，黑龙江93例，四川88例，吉林81例，山东78例，江西55例，新疆33例，广东24例，海南21例，天津19例，广西18例，河南17例，湖北16例，甘肃16例，河北15例，贵州12例，内蒙古10例，陕西8例，浙江3例，湖南2例，重庆1例）。"

    asysplt = re.split("（", rawAsym)
    ttlAsym = int(re.sub(u"([^\u0030-\u0039])", "", re.split("，", asysplt[1])[-1]))
    print(ttlAsym)

    asyName, asyCase = [], []
    asyProv = re.split('，', asysplt[2])
    for asy in cassplt:
        asynm = re.sub(u"([^\u4e00-\u9fa5])", "", asy)
        asyName.append(asynm[0:-1])
        asyCase.append(int(re.sub(u"([^\u0030-\u0039])", "", asy)))

    print(asyName, asyCase)


def main():

    #skimData()
    loadCovidData()
    #loadCovidList()

if __name__ == '__main__':
    main()
