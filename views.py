from django.http import HttpResponse, JsonResponse

#import requests

#from bs4 import BeautifulSoup

import csv
import pandas as pd
import requests
import io


def index(request):
    url='https://raw.githubusercontent.com/jooeungen/coronaboard_kr/master/kr_daily.csv'
    c= requests.get(url).content
    s=pd.read_csv(io.StringIO(c.decode('utf-8')))
    s=s.to_json()
    return JsonResponse({'search list' : s}, status=200)
    
    #return HttpResponse("Hello, world. You're at the polls index.")