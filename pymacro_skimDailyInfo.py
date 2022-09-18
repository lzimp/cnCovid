

import os, requests, random, re
import pandas as pd
import urllib.request
import numpy as np
import time
from bs4 import BeautifulSoup
from datetime import datetime as dt
from csv import DictWriter

def skimDayData(fl="nhcRaw2022/7月19日.txt"):

    rawfile = open(fl, "r")
    rflinfo = rawfile.read()
    dayinfo = rflinfo.split("\n")
    rawfile.close()

    rawdata = dayinfo[0]
    
    lclProv = []
    rawsplt = re.split('。|；', rawdata)
    for s in rawsplt:
        if '本土病例' in s:
            lclProv.append(s)
        else:
            pass

    #print(lclProv)
    prvList = []
    prvsplt = re.split('（|），', lclProv[0])
    for lcl in prvsplt:
        prvList.append(lcl)

    # List for the context in the first paragraph: 每日新增确诊病例书、无症状转确诊病例数，
    # 及其分省信息。
    # 0: 全国总日增本土病例，    
    #print(prvList)
    ttlCase = int(re.sub(u"([^\u0030-\u0039])", "", prvList[0]))
    #print(ttlCase, type(ttlCase))

    # 1: 本土分省日增病例，
    prvName, prvCase = [], []
    cassplt = re.split('，', prvList[1])
    for prv in cassplt:
        prvnm = re.sub(u"([^\u4e00-\u9fa5])", "", prv)
        prvName.append(prvnm[0:-1])
        prvCase.append(int(re.sub(u"([^\u0030-\u0039])", "", prv)))

    #print(prvName, prvCase)

    # 2: 全国无症状转确诊病例数，3: 分省信息
    ttlAtcf = int(re.sub(u"([^\u0030-\u0039])", "", prvList[2]))
    atcName, atcCase = [], []
    atcsplt = re.split('，', prvList[3])
    for prv in atcsplt:
        atcnm = re.sub(u"([^\u4e00-\u9fa5])", "", prv)
        atcName.append(atcnm[0:-1])
        atcCase.append(int(re.sub(u"([^\u0030-\u0039])", "", prv)))

    #print(atcName, atcCase)

    rawAsym = dayinfo[4]
    #print(rawAsym)

    asysplt = re.split("（", rawAsym)
    ttlAsym = int(re.sub(u"([^\u0030-\u0039])", "", re.split("，", asysplt[1])[-1]))

    #print(asysplt, ttlAsym)

    asyName, asyCase = [], []
    asyProv = re.split('，', asysplt[2])
    #print(asyProv)
    for asy in asyProv:
        asynm = re.sub(u"([^\u4e00-\u9fa5])", "", asy)
        asyName.append(asynm[0:-1])
        asyCase.append(int(re.sub(u"([^\u0030-\u0039])", "", asy)))

    #print(asyName, asyCase)

    return prvName, prvCase, atcName, atcCase, asyName, asyCase

def skimSchData(fl="shcRaw2022/08月01日.txt"):

    rawfile = open(fl, "r")
    rflinfo = rawfile.read()
    dayinfo = rflinfo.split("\n")
    rawfile.close()

    rawdata = dayinfo[0] + dayinfo[1]
    
    lclProv = []
    rawsplt = re.split('，', rawdata)
    #print(rawsplt)
    for s in rawsplt:
        if '新增本土' in s:
            lclProv.append(s)
        else:
            pass

    prvList = []
    prvsplt = re.split('（|），', lclProv[0])
    for lcl in prvsplt:
        prvList.append(lcl)
    
    print(prvList)
    # List for the context in the first paragraph: 每日新增确诊病例书、无症状转确诊病例数，
    # 及其分省信息。
    # 0: 全国总日增本土病例，    
    #print(prvList)
    ttlCase = int(re.sub(u"([^\u0030-\u0039])", "", prvList[0]))
    #print(ttlCase, type(ttlCase))

    # 1: 本土分省日增病例，
    prvName, prvCase = [], []
    if len(prvList) == 2:
        prvnm = prvList[1]
        prvName.append(prvnm[1:-1])
        prvCase.append(ttlCase)
    elif len(prvList) > 2:
        cassplt = re.split('，', prvList[1])
        for prv in cassplt:
            prvnm = re.sub(u"([^\u4e00-\u9fa5])", "", prv)
            prvName.append(prvnm[0:-1])
            prvCase.append(int(re.sub(u"([^\u0030-\u0039])", "", prv)))

    print(prvName, prvCase)

#    # 2: 全国无症状转确诊病例数，3: 分省信息
#    ttlAtcf = int(re.sub(u"([^\u0030-\u0039])", "", prvList[2]))
#    atcName, atcCase = [], []
#    atcsplt = re.split('，', prvList[3])
#    for prv in atcsplt:
#        atcnm = re.sub(u"([^\u4e00-\u9fa5])", "", prv)
#        atcName.append(atcnm[0:-1])
#        atcCase.append(int(re.sub(u"([^\u0030-\u0039])", "", prv)))
#
#    #print(atcName, atcCase)

    rawAsym = prvList[1]
    #print(rawAsym)

    asysplt = re.split("（", rawAsym)
    ttlAsym = int(re.sub(u"([^\u0030-\u0039])", "", re.split("，", asysplt[1])[-1]))

    #print(asysplt, ttlAsym)

    asyName, asyCase = [], []
    asyProv = re.split('，', asysplt[2])
    #print(asyProv)
    for asy in asyProv:
        asynm = re.sub(u"([^\u4e00-\u9fa5])", "", asy)
        asyName.append(asynm[0:-1])
        asyCase.append(int(re.sub(u"([^\u0030-\u0039])", "", asy)))

    #print(asyName, asyCase)

    return prvName, prvCase, atcName, atcCase, asyName, asyCase


def dayDataSave(fl = "nhcRaw2022/7月19日.txt"):

    prvInfo = pd.read_csv("prvList.txt", sep="\s+", header=None)
    prvIndx = pd.Index(prvInfo[0])
    #print(prvInfo[0])

    #fl = "nhcRaw2022/7月19日.txt"
    prvName, prvCase, atcName, atcCase, asyName, asyCase = skimDayData(fl)
    #print(prvName, prvCase, atcName, atcCase, asyName, asyCase)

    date = re.split('月', fl[11:-5])
    #tday = dt.strptime('22-' + date[0].zfill(2)+ '-' + date[1].zfill(2), '%y-%m-%d').date()
    tday = dt.strptime('22-%s-%s'%(date[0], date[1]), '%y-%m-%d').date()
    #print(type(tday))
 
    ipos = 0
    for prv in list(set(prvName + atcName + asyName)):

        if prv in prvName:
            prvpos = prvCase[prvName.index(prv)]
        else:
            prvpos = 0

        if prv in asyName:
            prvasy = asyCase[asyName.index(prv)]
        else:
            prvasy = 0

        if prv in atcName:
            prvatc = atcCase[atcName.index(prv)]
        else:
            prvatc = 0
        #print(prv, prvpos, prvasy, prvatp)

        prvidx = prvIndx.get_loc(prv)
        flhead = prvInfo[1][prvidx]
        #print(prv, prvidx, flhead, type(flhead))
        svFile = "nhcDat2022/covid19_" + flhead + ".csv"
        if os.path.exists(svFile):
            df = pd.read_csv(svFile)
            #print(df, type(df))
            # get the date of the last entry
            #ltdate = df["date"].iloc[len(df.index)-1]
            # get the list of the date for all entries
            ltdate = [x for x in df.date]
            #if ltdate == str(tday):
            #    print("the data is latest already!")
            if str(tday) in ltdate:
                print("data from %s was recorded already"%(str(tday)))
            else:
                print("write the data from %s!"%(str(tday)))
                fields = ['date', 'con', 'asy', 'atc']
                dict = {'date':tday, 'con':prvpos, 'asy':prvasy, 'atc':prvatc}
                with open(svFile, 'a') as flobject:
                    dctobject = DictWriter(flobject, fieldnames = fields)
                    dctobject.writerow(dict)

                    flobject.close()

        else:
            dtHeader = {'date':[tday], 'con':[prvpos], 'asy':[prvasy], 'atc':[prvatc]}
            prvData = pd.DataFrame(dtHeader)
            #prvData[0] = [prvpos, prvasy, prvatp]

            print(prvData)

            #prvData.to_pickle(svFile)
            prvData.to_csv(svFile, index=False)


def main():

    flList = os.listdir('nhcRaw2022/')
    flList.sort(key=lambda x:str(x.split('.')[0]))
    ##print(flList)
    #for fn in flList:
    #    fl = "nhcRaw2022/" + fn
    #    print(fl)
    #    dayDataSave(fl)

    fl = "nhcRaw2022/" + flList[-1]
    dayDataSave(fl)

    #sfl = "shcRaw2022/08月19日.txt"
    #skimSchData(sfl)

if __name__ == '__main__':
    main()
