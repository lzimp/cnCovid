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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#==============================================================
#plt.rcParams["font.sans-serif"]=["fangsong_GB2312"] #设置字体
plt.rcParams["font.sans-serif"]=["FangSong"] #设置字体
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
    totAtc, totAsy = -sum(atcCase), sum(asyCase)
    rateAtc = 100.*totAtc / totAsy

    fig, axs = plt.subplots(1, 1, constrained_layout=True)
    tday = str(dt.date.today())
    axs.text(0.75, 0.95, 'by @lzimp (%s)'%(tday), transform=axs.transAxes, fontsize=8, color='gray', alpha=0.25, ha='center', va='center', rotation='0')

    axs.text(0.45, 0.95, '%.2f%%'%(rateAtc), transform=axs.transAxes, fontsize=12, color='red', alpha=0.75, ha='center', va='center', rotation='0')
    axs.bar(tsdate, prvpstv, alpha=0.75, label='%s 日增阳性'%(prname))
    axs.plot(tsdate, prvravg, '-or', ms=3, label='%s 七日平均'%(prname))
    axs.bar(tsdate, conCase, color='m', alpha=0.35, label='%s 日增确诊'%(prname))
    axs.bar(tsdate, asyCase, color='g', alpha=0.35, label='%s 日增无症状'%(prname))
    axs.bar(tsdate, atcCase, color='orange', alpha=0.35, label='%s 无症状转确诊'%(prname))

    #axs.tick_params(axis='x', labelrotation=45, labelright=True)
    axs.set_xticklabels(axs.get_xticklabels(), rotation=30, va='top', ha='center') # center or right
    axs.set_xlabel("Date", fontsize=16, ha='right', x=1.0)
    axs.set_ylabel("Number of Daily Cases", fontsize=16, ha='right', y=1.0)

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
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    xmin, xmax = axs.get_xlim()
    axs.plot([xmin, xmax], [0, 0], 'black')
    axs.set_xlim(xmin, xmax)

    axs.legend(lns1+lns2, lbs1+lbs2, loc='best', facecolor='whitesmoke', edgecolor='black', fontsize=10)

    #plt.show()
    plt.savefig("nhcRes2022/%s_pstvStats2207.png"%(pname), dpi=200)
    plt.close()

    return prname, cvDat.con.iloc[-1], cvDat.asy.iloc[-1], cvDat.atc.iloc[-1], rateAtc, prvrTot.iloc[-1]

def dailyInfo(dtInfo):


    dtInfo = np.array(dtInfo)
    #print(dtInfo)
    rateAtc = [float(x) for x in dtInfo[:, 4]]
    totCase = [float(x) for x in dtInfo[:, 5]]
    tday = str(dt.date.today())
    #print(tday)

    fig, axs = plt.subplots(1, 1, constrained_layout=True)

    axs.plot(dtInfo[:, 0], rateAtc, 'or', alpha=0.75, label='无症状转确诊（自7月19日）')
    axs.text(0.80, 0.75, 'by @lzimp (%s)'%(tday), transform=axs.transAxes, fontsize=8, color='gray', alpha=0.25, ha='center', va='center', rotation='0')

    ax2 = axs.twinx()
    ax2.set_ylabel("累计总数", color='c', fontsize=16, horizontalalignment='right', y=1.0)
    ax2.bar(dtInfo[:, 0], totCase, alpha=0.75, label='阳性总数（自7月19日）')

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
    flList = os.listdir('nhcDat2022/')
    plist = []
    for fl in flList:
        name = fl[8:12]
        plist.append(name)
#    plist = ["hana", "sich"]
    
    dtInfo = []
    for pname in plist:
        prvfile = "nhcDat2022/covid19_%s.csv"%(pname)
        print(prvfile)
        prnm, con, asy, atc, rateAtc, totCase = prvDataStats(prvfile, pname)
        dtInfo.append([prnm, con, asy, atc, rateAtc, totCase])

    #print(dtInfo)
    dailyInfo(dtInfo)

if __name__ == '__main__':

    main()
