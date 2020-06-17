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
    #new_krdaily_list=list(set([tuple(set(item)) for item in krdaily_list]))

    obj_num=krdaily.objects.all().count()
    latest_krdaily_list=new_krdaily_list[obj_num-5:]

    template = loader.get_template('polls/main.html')
    context={
        'latest_krdaily_list':latest_krdaily_list,
    }
    return HttpResponse(template.render(context, request))


def regions(request):
    template = loader.get_template('polls/regions.html')
    context={
    }
    return HttpResponse(template.render(context, request))


def nations(request):
    template = loader.get_template('polls/nations.html')
    context={
    }
    return HttpResponse(template.render(context, request))


def departure(request):
    from polls.models import Country

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
                    p=Country(name=countryName, information=infor, safety=0, entrance="격리")                        
                elif countryName=="미국(United States of America)":
                    plus_infor="\n\n***14일 이내 중국, 이란, 유럽국가, 브라질을 방문/환승한 외국인 입국 금지***\n***괌, 하와이 입국은 격리***"
                    p=Country(name=countryName, information=infor+plus_infor, safety=0, entrance="예외")                        
                else:
                    p=Country(name=countryName, information=infor, safety=0, entrance="불가능")

                p.save()
    """

    Country_departure=Country.objects.all()
    template = loader.get_template('polls/departure.html')
    context={
        'Country_departure':Country_departure,
    }
    return HttpResponse(template.render(context, request))