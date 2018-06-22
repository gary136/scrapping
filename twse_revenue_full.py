import pandas as pd
import requests
from io import StringIO
import time

year = 105
month_range = list(range(1, 13))
full = []
for t in month_range:
    month = t
    url = 'http://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'# 國內_0.html; 國外_1.html
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers)
    r.encoding = 'big5'
    print('downloading from web....')
    html_df = pd.read_html(StringIO(r.text))
    print('download has finished')
    time.sleep(3)

    list_index = list(range(2, len(html_df), 2)) 
    list_n = list(range(len(html_df)//2))
    column_default = ['公司代號', '公司名稱', '%d月營收' % (t)]
    for i in list_index:
        df = html_df[i]
        column_cut = list(range(3, df.columns[-1]+1))# 國內11; 國外_9
        for j in column_cut:
            df= df.drop(j, axis = 1) 
        df.columns = column_default
        df.drop(0, axis = 0, inplace = True)        
        df.drop(1, axis = 0, inplace = True)
        df = df[df['公司代號'] != '合計']
        df = df[df['公司代號'].isnull() != True]
        df = df[df['公司代號'] != '公司代號']
        list_n[i//2 - 1] = df
                
    temp = pd.concat(list_n)
    full.append(temp)
    print('report_%s_%s done' % (year, month))

for k in range(len(full)-1):
    full[0] = pd.merge(full[0], full[k+1], how = 'outer')
sales_m = full[0]    
print(sales_m)

sales_m.to_csv('sales_m_%s.csv' % (year), index = False)




