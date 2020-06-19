from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
# Create your views here.
import csv
import pandas as pd
import requests
import io
from matplotlib import pyplot as plt
from urllib.parse import urlencode, quote_plus
from bs4 import BeautifulSoup
import datetime
import time
from datetime import timedelta


def main(request):
    from polls.models import krdaily
    
    url='https://raw.githubusercontent.com/jooeungen/coronaboard_kr/master/kr_daily.csv'
    c=requests.get(url).content
    s=pd.read_csv(io.StringIO(c.decode('utf-8')))
    
    krdaily_list=krdaily.objects.all()
    krdaily_list.delete()
    
    for data in s.values:
        p=krdaily(kr_date=data[0], kr_confirmed=data[1], kr_death=data[2], kr_released=data[3], kr_candidate=data[4], kr_negative=data[5])
        p.save()
    
    new_krdaily_list=krdaily.objects.all()

    obj_num=krdaily.objects.all().count()
    latest_krdaily_list=new_krdaily_list[obj_num-5:]

    template = loader.get_template('polls/main.html')
    context={
        'latest_krdaily_list':latest_krdaily_list,
    }
    return HttpResponse(template.render(context, request))


def regions(request):
    from polls.models import kr_region
    """
    url='https://raw.githubusercontent.com/jooeungen/coronaboard_kr/master/kr_regional_daily.csv' 
    c= requests.get(url).content
    s=pd.read_csv(io.StringIO(c.decode('utf-8'))) #지역별 코로나 확진자
    
    kr_regional_list=kr_region.objects.all()
    kr_regional_list.delete()

    for data in s.values:
        p=kr_region(kr_date=data[0], kr_region=data[1], kr_confirmed=data[2], kr_death=data[3], kr_released=data[4])
        p.save()
    """
    t = datetime.datetime.today()
    yesterday=t - timedelta(days=1)
    today_date=time.strftime('%Y-%m-%d', time.localtime(time.time()))
    yesterday_date=yesterday.strftime('%Y-%m-%d')

    kr_regional_list=kr_region.objects.all() #국내 지역별 현황
    obj_num=kr_region.objects.all().count() 
    yesterday_list=kr_regional_list[obj_num-36:obj_num-18] #어제의 현황
    today_list=kr_regional_list[obj_num-18:] #오늘의 현황

    daynum_list=[] #지역별 오늘의 확진자수 리스트
    for i in range(0, 18):
        daynum_list.append(int(today_list[i].kr_confirmed)-int(yesterday_list[i].kr_confirmed))

    i=0
    for today in today_list: #today_list에 오늘 확진자수를 넣어준다.
        today.kr_released=daynum_list[i]
        i=i+1
        today.save()

    template = loader.get_template('polls/regions.html')
    context={
        'yesterday_date':yesterday_date,
        'today_date':today_date,
        'today_list':today_list,
        'yesterday_list':yesterday_list,
    }
    return HttpResponse(template.render(context, request))


def nations(request):
    from polls.models import World_daily
    """
    worlddaily_list=World_daily.objects.all()
    worlddaily_list.delete()

    url='https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    c=requests.get(url).content
    s=pd.read_csv(io.StringIO(c.decode('utf-8')))

    t = datetime.datetime.today()
    b_yesterday=t - timedelta(days=3)
    yesterday=t - timedelta(days=2)
    today=t - timedelta(days=1)
    yesterday_date=yesterday.strftime('%Y-%m-%d')
    b_yesterday_date=b_yesterday.strftime('%Y-%m-%d')
    today_date=today.strftime('%Y-%m-%d')


    for data in s.values:
        if today_date==data[3]:
            p=World_daily(world_country=data[2], world_today_date=data[3], world_total_confirmed=data[4], world_new_cases=data[5], world_total_death=data[6], world_new_death=data[7], world_deaths_rate=data[10])
            p.save()
        elif yesterday_date==data[3]:
            p=World_daily(world_country=data[2], world_today_date=data[3], world_total_confirmed=data[4], world_new_cases=data[5], world_total_death=data[6], world_new_death=data[7], world_deaths_rate=data[10])
            p.save()
        elif b_yesterday_date==data[3]:
            p=World_daily(world_country=data[2], world_today_date=data[3], world_total_confirmed=data[4], world_new_cases=data[5], world_total_death=data[6], world_new_death=data[7], world_deaths_rate=data[10])
            p.save()
    """

    t = datetime.datetime.today()
    b_yesterday=t - timedelta(days=3)
    yesterday=t - timedelta(days=2)
    today=t - timedelta(days=1)
    yesterday_date=yesterday.strftime('%Y-%m-%d')
    b_yesterday_date=b_yesterday.strftime('%Y-%m-%d')
    today_date=today.strftime('%Y-%m-%d')

    World_daily_data=World_daily.objects.all()

    template = loader.get_template('polls/nations.html')
    context={
        'b_yesterday_date':b_yesterday_date,
        'yesterday_date':yesterday_date,
        'today_date':today_date,
        'World_daily_data':World_daily_data,
    }

    return HttpResponse(template.render(context, request))


def departure(request):
    from polls.models import Country, World_daily
    """
    IDs=[] #id 담을 리스트 (내용중복방지)
    C_country={}

    Country_list=Country.objects.all()
    Country_list.delete()

    api_key='Z1ghH%2Bq0HwropYoFYpaNT2OJis%2BBY%2Fz3LeC2HEMOJuTX6wfLmLrvIdVSaxW7hXADq%2Fw8rNuLZRRI9xL0bPG04A%3D%3D'
    api_key_decode=requests.utils.unquote(api_key)
    url = 'http://apis.data.go.kr/1262000/SafetyNewsList/getCountrySafetyNewsList'
    for k in range(1, 11):
        queryparam = '?'+ urlencode({ quote_plus('ServiceKey') : api_key_decode, quote_plus('content') : '입국', quote_plus('numOfRows'):'150', quote_plus('pageNO'): str(k)})
        response = requests.get(url+queryparam)
        soup = BeautifulSoup(response.content, 'html.parser')
        for items in soup.find_all('item') : #item 단락 파싱
            id=items.find('id').text
            if id not in IDs:
                IDs.append(id) #ID 리스트에 id삽입(같은내용 중복되지 않도록)
                Name=items.find('countryname').text
                E_Name=items.find('countryenname').text
                countryName=Name+"("+E_Name+")"
                infor=items.find('content').text

                if countryName=="홍콩(중국)(China)"or countryName=="캄보디아(Cambodia)"or countryName=="영국(United Kingdom)" :
                    p=Country(name=countryName, information=infor, safety=3, entrance="격리") 
                    p.save()                       
                elif countryName=="미국(United States of America)":
                    plus_infor="\n\n***14일 이내 중국, 이란, 유럽국가, 브라질을 방문/환승한 외국인 입국 금지***\n***괌, 하와이 입국은 격리***"
                    p=Country(name=countryName, information=infor+plus_infor, safety=1, entrance="예외") 
                    p.save()                       
                else:
                    p=Country(name=countryName, information=infor, safety=5, entrance="불가능")
                    p.save()
    """    

    Country_departure=Country.objects.all()
    template = loader.get_template('polls/departure.html')
    exp="예외"
    avail="격리"
    unavail="불가능"
    context={
        'exp':exp,
        'avail':avail,
        'unavail':unavail,
        'Country_departure':Country_departure,
    }
    return HttpResponse(template.render(context, request))