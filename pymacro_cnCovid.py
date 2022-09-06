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
        self.covidData = pd.read_csv(self.file)


def hnDataStats(hnfile, pname):
    #if pname == "hana":
    #    pnm = "HN"
    #elif pname == "sich":
    #    pnm = "SC"


    hnCovid = covidData(hnfile)
    hnCovid.loadData()
    cvDat = hnCovid.covidData
    tsdate = []
    for date in cvDat['date']:
        test = dt.datetime.strptime('%s'%(date), '%Y-%m-%d').date()
        #print(test)
        tsdate.append(test)

    #print(tsdate[0], type(tsdate[0]))

    cvDat['pos'] = cvDat['con'] + cvDat['asy'] - cvDat['atc']
    hnpstv = cvDat['pos']
    cvDat['tot'] = cvDat['pos'].cumsum()
    hnrTot = cvDat['tot']
    hnravg = cvDat['pos'].rolling(window=7).mean()

    #print(lzravg, cgravg)
    print(cvDat)

#    pmdl = SARIMAX(hnpstv, order=(1, 1, 1), seasonal_order=(0, 0, 0, 0))
#    fmdl = pmdl.fit(disp=False)
#    ndays = len(hnpstv)
#    fdate, fcase = [], []
#    fdt = tsdate[ndays-1]
#    for fday in range(ndays, ndays+10):
#        case = fmdl.predict(fday, fday)
#        fdt = fdt + dt.timedelta(days=1)
#        fdate.append(fdt)
#        for cs in case.tolist():
#            #print(cs)
#            fcase.append(cs)
#
#    #=====================================================
#    # creat and train forecaster
#    regressor = RandomForestRegressor(random_state=123, max_depth=3, n_estimators=20)
#    forecaster = ForecasterAutoreg(regressor=regressor, lags=5)
#    forecaster.fit(y=hnpstv)
#    #print(forecaster)
#    preCases = forecaster.predict(steps=10)
#    #print(preCases)

    fig, axs = plt.subplots(1, 1, constrained_layout=True)
    tday = str(dt.date.today())
    axs.text(0.75, 0.95, 'by @lzimp (%s)'%(tday), transform=axs.transAxes, fontsize=8, color='gray', 
            alpha=0.25, ha='center', va='center', rotation='0')

    axs.bar(tsdate, hnpstv, alpha=0.75, label='%s daily pos'%(pname))
    axs.plot(tsdate, hnravg, '-or', label='%s 7days avg'%(pname))
    #axs.plot(fdate, fcase, '--gd', label='simple prediction')
    #axs.plot(fdate, preCases, '--gd', label='simple prediction')

    axs.tick_params(axis='x', labelrotation=45)
    axs.set_xlabel("Date", fontsize=16, horizontalalignment='right', x=1.0)
    axs.set_ylabel("Number of Daily Cases", fontsize=16, horizontalalignment='right', y=1.0)

    ax2 = axs.twinx()
    ax2.set_ylabel("Number of Total Cases", color='c', fontsize=16, horizontalalignment='right', y=1.0)
    ax2.plot(tsdate, hnrTot, '--c', label='%s total (TD)'%(pname))

    axs.legend(loc='upper left', facecolor='whitesmoke', edgecolor='black', fontsize=10)
    ax2.legend(loc='center left', facecolor='whitesmoke', edgecolor='black', fontsize=10)
    plt.grid(axis='x', which='major', linestyle='--')
    plt.grid(axis='y', which='major', linestyle='--')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))

    #plt.show()
    plt.savefig("nhcRes2022/%s_pstvStats2207.png"%(pname), dpi=200)


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
    #plist = ["hana", "sich"]
    
    for pname in plist:
        hnfile = "nhcDat2022/covid19_%s.csv"%(pname)
        print(hnfile)
        hnDataStats(hnfile, pname)

if __name__ == '__main__':

    main()
