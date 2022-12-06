# macro for the data (xlsx) of Lanzhou Covid19 in July
# 
# file requrie: csv file for data analysis
#
# Author: D.X.~Lin (Lanzhou)
# Date: Sep.05, 2022
#==============================================================

import os, sys, platform, math, time
import datetime as dt
import pickle as pckl
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#==============================================================
#plt.rcParams["font.sans-serif"]=["fangsong_GB2312"] #设置字体
plt.rcParams["font.sans-serif"]=["FangSong"] #设置字体
#zhfont = mpl.font_manager.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', size=10)
#plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题

class covidData(object):
    def __init__(self, dtfile):
        self.file = dtfile

    def loadData(self):
        prvdata = pd.read_csv(self.file)
        # convert the string of date into datetime format
        prvdata['date'] = pd.to_datetime(prvdata['date'], format='%Y-%m-%d')

        # insert the missing date into the data, and the number of cases is zero!
        r = pd.date_range(start=prvdata.date.min(), end=prvdata.date.max())
        prvdata = prvdata.set_index('date').reindex(r).fillna(0).rename_axis('date').reset_index()
        #print(prvdata)

        self.covidData = prvdata

def prvDataStats(prvfile, pname):

    # consider to use the Chinese characters or full Name in the legend
    prvInfo = pd.read_csv("prvList.txt", sep="\s+", header=None)
    prvIndx = pd.Index(prvInfo[1])

    prvidx = prvIndx.get_loc(pname)
    prname = prvInfo[0][prvidx]
    #print(pname, prname)

    prvCovid = covidData(prvfile)
    prvCovid.loadData()
    cvDat = prvCovid.covidData
    tsdate = cvDat['date']

    cvDat['pos'] = cvDat['con'] + cvDat['asy'] - cvDat['atc']
    prvpstv = cvDat['pos']
    cvDat['tot'] = cvDat['pos'].cumsum()
    prvrTot = cvDat['tot']
    prvravg = cvDat['pos'].rolling(window=7).mean()
    #print(cvDat)
    conCase, asyCase = cvDat['con'], cvDat['asy']
    atcCase = [-x for x in cvDat['atc']]
    totAtc, totAsy = sum(cvDat['atc']), sum(cvDat['asy'])
    rateAtc = 100.*totAtc / totAsy
    if totAtc == 0:
        dratAtc = 0
    else:
        dratAtc = rateAtc*np.sqrt(1/totAtc + 1/totAsy)
    #print(rateAtc, dratAtc)
    totCon = sum(cvDat['con'])
    totPos = sum(cvDat['pos'])
    fstCon = totCon - totAtc
    fnlAsy = totAsy - totAtc


    #print("-------------------")
    #print("%d, %d, %d, %d"%(totPos, fstCon, totAtc, fnlAsy))

    #fig, axs = plt.subplots(2, 3, constrained_layout=True) 
    fig = plt.figure()
    fig.set_figheight(6)
    fig.set_figwidth(9)
    gd1 = plt.subplot2grid(shape=(2,3), loc=(0,0), colspan=2, rowspan=2)
    axs = fig.add_subplot(gd1, layout="contrained")
    gd3 = plt.subplot2grid(shape=(2,3), loc=(0,2), colspan=1, rowspan=1)
    ax3 = fig.add_subplot(gd3, layout="contrained")
    fig.set_constrained_layout(False)

    tday = str(dt.date.today())
    axs.text(0.75, 0.95, 'by @lzimp (%s)'%(tday), transform=axs.transAxes, fontsize=8, color='gray', alpha=0.25, ha='center', va='center', rotation='0')

    #axs.text(0.45, 0.95, '%.2f%%'%(rateAtc), transform=axs.transAxes, fontsize=12, color='red', alpha=0.75, ha='center', va='center', rotation='0')
    axs.bar(tsdate, prvpstv, alpha=0.75, label='%s 日增阳性'%(prname))
    axs.plot(tsdate, prvravg, '-or', ms=3, label='%s 七日平均'%(prname))
    axs.bar(tsdate, conCase, color='m', alpha=0.35, label='%s 日增确诊'%(prname))
    axs.bar(tsdate, asyCase, color='g', alpha=0.35, label='%s 日增无症状'%(prname))
    axs.bar(tsdate, atcCase, color='orange', alpha=0.35, label='%s 无症状转确诊'%(prname))

    #axs.tick_params(axis='x', labelrotation=45, labelright=True)
    locTicker = axs.get_xticks().tolist()
    axs.xaxis.set_major_locator(mticker.FixedLocator(locTicker))
    axs.set_xticklabels(axs.get_xticklabels(), rotation=30, va='top', ha='center') # center or right
    axs.set_xlabel("Date", fontsize=16, ha='right', x=1.0)
    axs.set_ylabel("Number of Daily Cases", fontsize=16, ha='right', y=1.0)
    miny, maxy = axs.get_ylim();

    if pname == "lazh":
        qindx = cvDat.index[cvDat['date'] == '2022-10-23'].tolist()
        axs.vlines(x=tsdate[qindx[0]], ymin=miny, ymax=150, color='orchid')
        axs.text(tsdate[qindx[0]], 155, "居家", color='orchid', size=12)

        rindx = cvDat.index[cvDat['date'] == '2022-11-13'].tolist()
        axs.vlines(x=tsdate[rindx[0]], ymin=miny, ymax=0, linestyles="dashed", color='orchid')
        #axs.text(tsdate[qindx[0]+2], -90, "部分解封", color='orchid', size=12)
        axs.vlines(x=tsdate[rindx[0]+7], ymin=miny, ymax=0, linestyles="dashdot", color='orchid')

        rrndx = cvDat.index[cvDat['date'] == '2022-12-05'].tolist()
        axs.vlines(x=tsdate[rrndx[0]], ymin=miny, ymax=0, color='orchid')
        axs.text(tsdate[qindx[0]+30], -90, "解封", color='orchid', size=12)

    axs.set_ylim(miny, maxy)
    sindx = cvDat.index[cvDat['date'] == '2022-10-01'].tolist()
    lstdt = len(tsdate)
    #print(tsdate[lstdt-1], type(tsdate[lstdt-1]))
    if pname not in ["lazh", "miya"]:
        axs.set_xlim(tsdate[sindx[0]], tsdate[lstdt-1]+pd.Timedelta(days=2))
    ax2 = axs.twinx()
    ax2.set_ylabel("Number of Total Cases", color='c', fontsize=16, horizontalalignment='right', y=1.0)
    ax2.plot(tsdate, prvrTot, '--c', label='%s 总阳性数'%(prname))

    #axs.legend(loc='upper left', facecolor='whitesmoke', edgecolor='black', fontsize=10)
    lns1, lbs1 = axs.get_legend_handles_labels()
    lns2, lbs2 = ax2.get_legend_handles_labels()

    plt.grid(axis='x', which='major', linestyle='--')
    plt.grid(axis='y', which='major', linestyle='--')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    if pname == "miya":
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    else:
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=20))
    xmin, xmax = axs.get_xlim()
    axs.plot([xmin, xmax], [0, 0], 'black')
    axs.set_xlim(xmin, xmax)

    axs.legend(lns1+lns2, lbs1+lbs2, loc='best', facecolor='whitesmoke', edgecolor='black', fontsize=10)

    ax3.pie([fstCon, totAtc, fnlAsy], labels=['直接确诊', '转确诊数', '无症状者'], explode=(0.1, 0.1, 0.1), autopct='%.2f%%')

    #plt.show()
    plt.tight_layout()
    plt.savefig("nhcRes2022/%s_pstvStats2207.png"%(pname), dpi=200)
    plt.close()

    return prname, cvDat.con.iloc[-1], cvDat.asy.iloc[-1], cvDat.atc.iloc[-1], rateAtc, dratAtc, prvrTot.iloc[-1]

def dailyInfo(dtInfo):


    dtInfo = np.array(dtInfo)
    #print(dtInfo)
    rateAtc = [float(x) for x in dtInfo[:, 4]]
    dratAtc = [float(x) for x in dtInfo[:, 5]]
    totCase = [float(x) for x in dtInfo[:, 6]]
    tday = str(dt.date.today())
    #print(tday)

    fig, axs = plt.subplots(1, 1, constrained_layout=True)

    #axs.plot(dtInfo[:, 0], rateAtc, 'or', alpha=0.75, label='无症状转确诊（自4月12日）')
    axs.errorbar(dtInfo[:, 0], rateAtc, yerr=dratAtc, fmt="o", color="r", capsize=4, alpha=0.75, label='无症状转确诊（自4月12日）')
    axs.text(0.80, 0.75, 'by @lzimp (%s)'%(tday), transform=axs.transAxes, fontsize=8, color='gray', alpha=0.25, ha='center', va='center', rotation='0')

    ax2 = axs.twinx()
    ax2.set_ylabel("累计总数", color='c', fontsize=16, horizontalalignment='right', y=1.0)
    ax2.bar(dtInfo[:, 0], totCase, alpha=0.75, label='阳性总数（自4月12日）')
    ax2.set_yscale('log')

    #axs.set_xticklabels(axs.get_xticklabels(), rotation=30, va='top', ha='center')
    axs.tick_params(axis='x', which='major', labelrotation=75, labelright=True)
    axs.set_xlabel('')
    axs.set_ylabel('总比率（%）')

    lns1, lbs1 = axs.get_legend_handles_labels()
    lns2, lbs2 = ax2.get_legend_handles_labels()

    axs.legend(lns1+lns2, lbs1+lbs2, loc='best', facecolor='whitesmoke', edgecolor='black', fontsize=10)

    plt.grid(axis='y', which='major', linestyle='--')
    #plt.show()
    plt.savefig("nhcRes2022/covid19_atcRate2022.png", dpi=200)

def main():

    #lzfile = "lanzhou_covid-19_202207.xlsx"
    #datCovid(lzfile)
    #lzDataStats(lzfile)
    #cdfile = "chengdu_covid19.xlsx"
    #cdDataStats(cdfile)
    #flList = ['covid19_miya.csv']
    flag = sys.argv[1]
    if flag == "all":
        flList = os.listdir('nhcDat2022/')
    else:
        cfl = 'covid19_' + sys.argv[1] + '.csv'
        flList = [cfl]

    plist = []
    for fl in flList:
        name = fl[8:12]
        plist.append(name)


#    plist = ["hana", "sich"]
    
    dtInfo = []
    for pname in plist:
        prvfile = "nhcDat2022/covid19_%s.csv"%(pname)
        if pname == "bitu":
            continue
        print(prvfile)
        prnm, con, asy, atc, rateAtc, dratAtc, totCase = prvDataStats(prvfile, pname)
        if pname in ["miya", "lazh"]:
            continue
        dtInfo.append([prnm, con, asy, atc, rateAtc, dratAtc, totCase])

    #print(dtInfo)
    if flag == "all":
        dailyInfo(dtInfo)

if __name__ == '__main__':

    main()
