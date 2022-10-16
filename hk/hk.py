import requests
from bs4 import BeautifulSoup
import numpy as np
import csv
import os
from pypinyin import pinyin, Style
from itertools import chain

hk_path = 'C:\\Users\\86155\\Desktop\\hk'
province=[]

def to_pinyin(s):
    return ''.join(chain.from_iterable(pinyin(s, style=Style.TONE3)))

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""


def fill_dict(soup):
    allUniv = []
    dict={}
    province = np.array([])
    province_temp=np.array([])
    th = soup.find_all('th')
    # print(lth)
    for lth in th:
        li = lth.find_all('li')
        # print(li)
        for lli in li:
            province_temp=np.append(province_temp,lli.text)
    province=province_temp[1:32]
    # print(province_temp[33])
    for i in list(province):
        dict[i] = []
    # print(dict)
    data = soup.find_all('tr')
    for tr in data:
        ltd = tr.find_all('td')
        # print(ltd)
        if len(ltd)==0:
            continue
        singleUniv = []
        for td in ltd:
            # print(td.text.strip())
            singleUniv.append(td.text.strip())
        allUniv.append(singleUniv)
    for item in allUniv:
        # print(item)
        dict[item[2]].append(item)
    # print(dict)
    # print(dict.key())
    return dict

def fill_csv(dict):
    for key in dict.keys():
        # print(dict[key])
        path = hk_path+'\\'+key+'.csv'
        f = open(path,'w+')
        # f=open('C:\\Users\\86155\\Desktop\\hk\\aaa.csv','w+')
        f.close()
        with open(path,'w+',newline='') as f:
            a = csv.writer(f)
            a.writerow(['全国排名','学校信息','省份','种类','总分','办学层次'])
            a.writerows(dict[key])

def read_csv():
    # print(province)
    key=[]

    file = os.listdir(hk_path)
    filename = file[1:]
    
    for i in filename:
        key.append(i[0:-4]) 
    sorted(key, key=to_pinyin)

    for each_key in key:
        path = hk_path+'\\'+each_key+'.csv'
        with open(path,'r',newline='') as f:
            a = csv.reader(f)
            # print(a)
            for line in a:
                # print(each_key,end='')
                info = line[1].split(' ')[0]
                if(info != '学校信息'):
                    print(each_key,end = ' ')
                    print(info)
            # print(a)
        # dict[each_key] = data
    
def main():
    url = 'https://www.shanghairanking.cn/rankings/bcur/2021'
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    dict = fill_dict(soup)
    fill_csv(dict)
    read_csv()

main()