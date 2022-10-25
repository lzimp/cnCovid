# a script to run the python macros for test

python3 pymacro_nhcData2022.py
#python3 pymacro_nhcData2209.py
python3 pymacro_skimDailyInfo.py
python3 pymacro_cnCovid.py all

convert -delay 90 -loop 0 nhcRes2022/*_pstvStats2207.png nhcRes2022/covid19_atcRate2022.png nhcRes2022/covid19_cn202210.gif

git add .
git commit -a -m "updated"
git push
