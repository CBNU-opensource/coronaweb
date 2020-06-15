#import xml.etree.ElementTree as ET
import pandas as pd
import sys
from urllib.request import urlopen, Request

import requests
from urllib.parse import urlencode, quote_plus

from bs4 import BeautifulSoup

api_key='Z1ghH%2Bq0HwropYoFYpaNT2OJis%2BBY%2Fz3LeC2HEMOJuTX6wfLmLrvIdVSaxW7hXADq%2Fw8rNuLZRRI9xL0bPG04A%3D%3D'
api_key_decode=requests.utils.unquote(api_key)

url = 'http://apis.data.go.kr/1262000/SafetyNewsList/getCountrySafetyNewsList'
queryparam = '?'+ urlencode({ quote_plus('ServiceKey') : api_key_decode, quote_plus('content') : '입국', quote_plus('numOfRows':'150')})

response = requests.get(url+queryparam)
soup = BeautifulSoup(response.content, 'html.parser')

country_name=[]
country_information=[]
country_safety=[]
country_entrance=[]
IDs=[]

for items in soup.find_all('item') : #item 단락 파싱
    id=items.find('id').text
    if id not in IDs:
        IDs.append(id)
        Name=items.find('countryname').text
        

    if country not in countryData :
        countryData.append(country)

for i in range(len(countryData)) : 
    print(countryData[i], end=" ")        #파싱한 데이터 출력

# print("\n헝가리"+"의 외국인 입국 관련 안내 사항입니다.\n")
# i=0
# for items in soup.find_all('item') :
#     country = items.find('countryname').text
#     if country == "헝가리" : 
#         id=items.find('id').text
#         if id not in IDs :
#             contents = items.find('content').text
#             IDs.append(id)
#             i=i+1
#             print("--------"+str(i)+"번째 알림--------\n")
#             print(contents)

IDs =[]
for i in range(len(countryData)):
    print("\n"+countryData[i]+"의 외국인 입국 관련 안내 사항입니다.\n")
    count=0
    for items in soup.find_all('item') :
        country = items.find('countryname').text
        if country == countryData[i] : 
            id=items.find('id').text
            if id not in IDs :
                contents = items.find('content').text
                IDs.append(id)
                count=count+1
                print("--------"+str(count)+"번째 알림--------\n")
                print(contents)


# xtree = ET.fromstring(response)
# xtree

# rows=[]

# #iterate through each node of the tree
# for node in xtree :
#     n_title=node.find('코로나').text
#     n_entrance = node.find('입국').text

#     rows.append({'title': n_title, 'entrance' : n_entrance})

# columns=['title', 'entrance']
# infors = pd.DataFrame(rows, columns=columns)
# infors.head(10)