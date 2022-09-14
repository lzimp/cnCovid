# python macro to get the information from nhc website
# download the covid19 information todate and save the daily
# information as a txt file
# Author: D.X. Lin (Lanzhou)
# Date: Sep. 05, 2022
#============================================================
# Suggest to run the macro: 
#       after 10:00 every day! 
#       or check the raw txt files 
#============================================================

import os, asyncio
from bs4 import BeautifulSoup
from pyppeteer import launcher
launcher.DEFAULT_ARGS.remove("--enable-automation")
from pyppeteer import launch
import datetime as dt
from lxml import etree


async def pyppteer_fetchUrl(url):

    browser = await launch({'headless': False,'dumpio':True, 'autoClose':True})
    page = await browser.newPage()

    await page.goto(url)
    await asyncio.wait([page.waitForNavigation()])
    str = await page.content()
    await browser.close()

    return str

def fetchUrl(url):
    return asyncio.get_event_loop().run_until_complete(pyppteer_fetchUrl(url))

def getPageUrl(nhctype):

    if nhctype == "cn":
        for page in range(1, 2):
            if page == 1:
                yield 'http://www.nhc.gov.cn/yjb/s7860/new_list.shtml'
            else:
                url = 'http://www.nhc.gov.cn/yjb/s7860/new_list_' + str(page) + '.shtml'
                yield url

    if nhctype == "sc":
        for page in range(1, 2):
            if page == 1:
                yield 'http://wsjkw.sc.gov.cn/scwsjkw/gzbd01/ztwzlmgl.shtml'
            else:
                url = 'http://wsjkw.sc.gov.cn/scwsjkw/gzbd01/ztwzlmgl_' + str(page) + '.shtml'
                yield url


def getTitleUrl(html, nhctype):

    bsobj = BeautifulSoup(html, 'html.parser')
    if nhctype == "cn":
        titleList = bsobj.find('div', attrs={"class": "list"}).ul.find_all("li")
    if nhctype == "sc":
        titleList = bsobj.find('div', attrs={"class": "wy_zt_ygzl"}).ul.find_all("li")

    for item in titleList:
        if nhctype == "cn":
            link = "http://www.nhc.gov.cn" + item.a["href"]
        if nhctype == "sc":
            link = "http://wsjkw.sc.gov.cn" + item.a["href"]

        date = item.span.text
        print("the item is: ", item, date, type(item))
        bttle = str(item).encode('utf-8')
        bttle = etree.HTML(bttle.decode('utf-8'))
        
        title = bttle.xpath('//div/a[@target="_blank"]')
        print("the title is: ", title)
        #title = item.a["title"]
        yield title, link, date

def getContent(html, nhctype):

    bsobj = BeautifulSoup(html, 'html.parser')
    if nhctype == 'cn':
        cnt = bsobj.find('div', attrs={"id": "xw_box"}).find_all("p")
    if nhctype == 'sc':
        cnt = bsobj.find('div', attrs={"class": "wy_contMain fontSt"}).find_all("p")
    s = []
    if cnt:
        for item in cnt:
            if item.text == "":
                continue
            s.append(item.text)
        return s

    return "failed to get the information!"

def saveData(path, flname, content):

    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + flname + ".txt", 'w', encoding='utf-8') as fl:
        str = '\n'
        fl.write(str.join(content))

def main():

    #path = "/data/jobs/csLearn/lzCovid19/stsData2022/"
    nhctype = "sc"
    if nhctype == "cn":
        path = "nhcRaw2022/"
    if nhctype == "sc":
        path = "shcRaw2022/"
    tdate = dt.date.today() #+ dt.timedelta(days=-1)
    print(tdate)

    for url in getPageUrl(nhctype):
        s = fetchUrl(url)

        for title, link, date in getTitleUrl(s, nhctype):
            print(title, link, date)
           
            #mon = int(date.split("-")[1])
            #day = int(date.split("-")[2])
            #if mon <= 6 and day < 1:
            #    break;
            if date != str(tdate):
                print("The following information is not for today!")
                break;

            html = fetchUrl(link)
            content = getContent(html, nhctype)
            print(content)

            if nhctype == 'cn':
                flname = title[2:-17]
                #print(flname)
                if flname[1] == "月":
                    mon = flname[0].zfill(2) + flname[1]
                else:
                    mon = flname[0:3]

                if flname[-3] == "月":
                    day = flname[-2].zfill(2) + flname[-1]
                else:
                    day = flname[-3:]
                flname = mon + day
            if nhctype == 'sc':
                flname = str(date.split("-")[1]) + "月" + str(date.split("-")[2]) + "日"
                print(flname)

            saveData(path, flname, content)
            print("--------"*20)

if __name__ == '__main__':

    main()
