import pandas as pd
import requests
from io import StringIO
import time
import os

os.chdir('C:\\Python\\Python36-32\\examples\\finance')
df_list = []
k_r = list(range(1,32))
default = []
for i in k_r:
   i = str(i).rjust(2,'0')
   default.append(i)
for num in default:
    url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=html&date=20180323&type=' + num
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    print('downloading from web')
    try:
        r = requests.get(url, headers)
        df = pd.read_html(StringIO(r.text))[0]
        print('download has finished')        
        df.columns = df.columns.droplevel()
        df.columns = df.columns.droplevel()
        df.drop(df.columns[[3,4,5,6,7,9,10,11,12,13,14,15]], axis=1, inplace = True)
        df_list.append(df)
        time.sleep(3)
        print('category ' + num + ' finished')
        
    except ValueError:
        print('No tables found')

print('all download finished')

temp = pd.concat(df_list)

print(temp)

temp.to_csv('price_%s.csv' % (url[-12:-8]), index = False)
