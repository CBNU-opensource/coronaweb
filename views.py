from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

#import requests

#from bs4 import BeautifulSoup

import csv
import pandas as pd
import requests
import io


def index(request):
    from polls.models import kr_region

    url='https://raw.githubusercontent.com/jooeungen/coronaboard_kr/master/kr_regional_daily.csv' 
    c= requests.get(url).content
    s=pd.read_csv(io.StringIO(c.decode('utf-8'))) #지역별 코로나 확진자
    
    kr_regional_list=kr_region.objects.all()
    kr_regional_list.delete()

    for data in s.values:
        p=kr_regional_list.create(kr_date=data[0], kr_region=data[1], kr_confirmed=data[2], kr_death=data[3], kr_released=data[4])
        p.save()

    kr_regional_list=kr_region.objects.all() #국내 지역별 현황
    obj_num=kr_region.objects.all().count() 
    yesterday_list=kr_regional_list[obj_num-36:obj_num-18] #어제의 현황
    today_list=kr_regional_list[obj_num-18:] #오늘의 현황

    daynum_list=[] #지역별 오늘의 확진자수 리스트
    str=''
    for i in range(0, 18):
        daynum_list.append(int(today_list[i].kr_confirmed)-int(yesterday_list[i].kr_confirmed))

    i=0
    for today in today_list: #today_list에 오늘 확진자수를 넣어준다.
        today.kr_released=daynum_list[i]
        i=i+1
        today.save()

    str="<p><pre>오늘의 지역별 확진자 현황</pre></p>"
    str+="<p><pre>지역 누적확진자수 사망자수 오늘확진자수</pre></p>"
    for region in today_list:
        str+="<p>{}&nbsp &nbsp &nbsp  {} &nbsp &nbsp &nbsp {} &nbsp &nbsp &nbsp &nbsp{}<br>".format(region.kr_region, region.kr_confirmed, region.kr_death, region.kr_released)
        str+="</p>"

    return HttpResponse(str)
