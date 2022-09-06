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

class covidData(object):
    def __init__(self, dtfile):
        self.file = dtfile

    def loadData(self):
        #self.covidData = pd.read_excel(self.file, engine='openpyxl')
        prvdata = pd.read_csv(self.file)
        #print(prvdata)
        fday = dt.datetime.strptime('%s'%(prvdata["date"][0]), '%Y-%m-%d').date()
        dtot = len(prvdata["date"])
        lday = dt.datetime.strptime('%s'%(prvdata["date"][dtot-1]), '%Y-%m-%d').date()

        dayd = (lday - fday).days + 1
        prvdata['date'] = pd.to_datetime(prvdata['date'], format='%Y-%m-%d')

        
        r = pd.date_range(start=prvdata.date.min(), end=prvdata.date.max())
        prvdata = prvdata.set_index('date').reindex(r).fillna(0).rename_axis('date').reset_index()
        #print(prvdata)

        self.covidData = prvdata

def prvDataStats(prvfile, pname):
    #if pname == "hana":
    #    pnm = "HN"
    #elif pname == "sich":
    #    pnm = "SC"


    prvCovid = covidData(prvfile)
    prvCovid.loadData()
    cvDat = prvCovid.covidData
    tsdate = cvDat['date']
    #for date in cvDat['date']:
    #    test = dt.datetime.strptime('%s'%(date), '%Y-%m-%d').date()
    #    #print(test)
    #    tsdate.append(test)

    #print(tsdate[0], type(tsdate[0]))

    cvDat['pos'] = cvDat['con'] + cvDat['asy'] - cvDat['atc']
    prvpstv = cvDat['pos']
    cvDat['tot'] = cvDat['pos'].cumsum()
    prvrTot = cvDat['tot']
    prvravg = cvDat['pos'].rolling(window=7).mean()

    #print(lzravg, cgravg)
    #print(cvDat)

    fig, axs = plt.subplots(1, 1, constrained_layout=True)
    tday = str(dt.date.today())
    axs.text(0.75, 0.95, 'by @lzimp (%s)'%(tday), transform=axs.transAxes, fontsize=8, color='gray', 
            alpha=0.25, ha='center', va='center', rotation='0')

    axs.bar(tsdate, prvpstv, alpha=0.75, label='%s daily pos'%(pname))
    axs.plot(tsdate, prvravg, '-or', label='%s 7days avg'%(pname))
    #axs.plot(fdate, fcase, '--gd', label='simple prediction')
    #axs.plot(fdate, preCases, '--gd', label='simple prediction')

    axs.tick_params(axis='x', labelrotation=45)
    axs.set_xlabel("Date", fontsize=16, horizontalalignment='right', x=1.0)
    axs.set_ylabel("Number of Daily Cases", fontsize=16, horizontalalignment='right', y=1.0)

    ax2 = axs.twinx()
    ax2.set_ylabel("Number of Total Cases", color='c', fontsize=16, horizontalalignment='right', y=1.0)
    ax2.plot(tsdate, prvrTot, '--c', label='%s total (TD)'%(pname))

    #axs.legend(loc='upper left', facecolor='whitesmoke', edgecolor='black', fontsize=10)
    lns1, lbs1 = axs.get_legend_handles_labels()
    lns2, lbs2 = ax2.get_legend_handles_labels()

    plt.grid(axis='x', which='major', linestyle='--')
    plt.grid(axis='y', which='major', linestyle='--')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))

    axs.legend(lns1+lns2, lbs1+lbs2, loc='best', facecolor='whitesmoke', edgecolor='black', fontsize=10)
    #fig.legend(loc='best', facecolor='whitesmoke', edgecolor='black', fontsize=10)
    #plt.show()
    plt.savefig("nhcRes2022/%s_pstvStats2207.png"%(pname), dpi=200)
    plt.close()

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
    
    for pname in plist:
        prvfile = "nhcDat2022/covid19_%s.csv"%(pname)
        print(prvfile)
        prvDataStats(prvfile, pname)

if __name__ == '__main__':

    main()
