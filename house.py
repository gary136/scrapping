import pandas as pd
import requests
from io import StringIO
import random
import time
import re
import numpy as np

# download the file
district_code = input('請輸入區域:')
start_page = input('請輸入開始頁數:')
end_page = input('請輸入結束頁數:')
scratch_range = range(int(start_page), int(end_page) + 1)

list_n = list(scratch_range)
              
for i in scratch_range:
    try:
        url = 'http://tradeinfo.sinyi.com.tw/itemList.html?a1=' + str(district_code) + '&s2=10501_10703&p=' + str(i)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers)
        print('downloading from web....')
        df = pd.read_html(StringIO(r.text))[-1]
        print('download has finished')

        # clean the data
        temp_column = []
        for j in range(len(df.columns.values)):
                    temp_column.append(df.columns.values[j].split()[0])
        df.columns = temp_column
        df['特殊'] = pd.Series(np.zeros(len(df)), index=df.index)
        for t in range(len(df)):
            df['特殊'][t] = 'None'
        for k in range(len(df)):
            if '備註' in df['年月'][k]: 
                df['特殊'][k-1] = df['年月'][k]
        df = df[df['地址'].isnull() != True]
    except AttributeError:
        print('AttributeError exception happens')
    except Exception:
        print('Unknown exception happens')
# join the data
    list_n[i-int(start_page)] = df
    print('page ' + str(i) + ' done')
    t = int(random.random() * 0) + 1
    time.sleep(t)
    
try:
    for i in range(len(list_n)):
        if type(list_n[i]) != pd.core.frame.DataFrame:
            del list_n[i]
except IndexError:
    pass

temp = pd.concat(list_n)
if 0 in temp.columns: 
    temp.drop([0, 1],axis=1,inplace=True)
temp = temp[temp['地址'].isnull() != True]
print(temp)
print('all pages done')
temp.to_csv('hou_%s.csv' % (district_code), index = False)
