#import xml.etree.ElementTree as ET
#import pandas as pd
import sys
from urllib.request import urlopen, Request

import requests
from urllib.parse import urlencode, quote_plus

from bs4 import BeautifulSoup

#db자동삽입용
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OSproject.settings")
import django
django.setup()

from corona.models import Country #모델 임포트

api_key='Z1ghH%2Bq0HwropYoFYpaNT2OJis%2BBY%2Fz3LeC2HEMOJuTX6wfLmLrvIdVSaxW7hXADq%2Fw8rNuLZRRI9xL0bPG04A%3D%3D'
api_key_decode=requests.utils.unquote(api_key)

IDs=[] #id 담을 리스트 (내용중복방지)
C_country={}

url = 'http://apis.data.go.kr/1262000/SafetyNewsList/getCountrySafetyNewsList'

def parse_api():
    for k in range(1, 11):
        queryparam = '?'+ urlencode({ quote_plus('ServiceKey') : api_key_decode, quote_plus('content') : '입국', quote_plus('numOfRows'):'150', quote_plus('pageNO'): str(k)})

        response = requests.get(url+queryparam)
        soup = BeautifulSoup(response.content, 'html.parser')

        for items in soup.find_all('item') : #item 단락 파싱
            id=items.find('id').text
            if id not in IDs:
                IDs.append(id) #ID 리스트에 id삽입(같은내용 중복되지 않도록)

                #한글+영어의 나라이름 파싱
                Name=items.find('countryname').text
                E_Name=items.find('countryenname').text
                countryName=Name+"("+E_Name+")"

                #나라 입국 정보 파싱
                infor=items.find('content').text

                #각 나라 정보를 나타내는 딕셔너리에 삽입
                C_country[countryName]=infor
                        
    return C_country

if __name__== '__main__':
    country_data_dict=parse_api()
    for n, i in country_data_dict.items():
        Country(name=n, information=i).save()