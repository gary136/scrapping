import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlretrieve
import os

os.chdir('C:\Python\Python36-32\examples\photo')
# 準備連線
start = input("請輸入網頁之編號 ")
startpagenum = int(start)
page = input("請輸入抓取頁數 ")
end = startpagenum - int(page)


# 清除非目標
def clean(key):
    for i in key:
        if ']' not in i or '公告' in i:
            del full[i]  

while startpagenum > end:
    url = 'https://www.ptt.cc/bbs/Beauty/index' + str(startpagenum) + '.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    print(str(startpagenum))
    # 抓當前頁面的連結標題及網址
    full = {}
    for i in soup.find_all('a'):
        if 'href' in i.attrs:
            title = i.get_text()
            link = i.get('href')
            rootlink = 'https://www.ptt.cc/'
            full[title] = rootlink + link

    fullKeys = list(full.keys())

    clean(fullKeys)

    fullKeys = list(full.keys())

    # 依序抓取連結的圖片
    # pageNum = 1
    for i in fullKeys:
        print("the current page is " + i)
        title = i
        r = requests.get(full[i])
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
        #     piclinks = []
            num = 1
            for j in soup.find_all('a'):
                if 'href' in j.attrs:
                    link = j.get('href')
                    if link.endswith('.jpg'):
        #                 piclinks.append(link)
                        try:
                            name = title + str(num) +'.jpg'
                            num += 1
                            urlretrieve (link, name)
                        except OSError:
                            print('Invalid argument')
        #     pageNum += 1
    print(str(startpagenum) + ' collection finished')
    
    startpagenum -= 1

