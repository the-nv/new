from django.shortcuts import render
from django.http import HttpResponse
import json
from .gann import GannSquare
import yfinance as yf
import requests
import numpy as np

gannSquare = GannSquare(1001)

def detail(request, securityName):
    context = {'securityId': securityName}

    security = yf.download(securityName, period='2y', interval='1d', threads=True)

    security_dict = security.to_dict()
    security_json = security.to_json()

    return HttpResponse(security_json)

def detail2(request, securityId):
    context = {'securityId': securityId}

    security = yf.download('RELIANCE.NS', period='1mo', interval='1d', threads=True)

    security_dict = security.to_dict()
    security_json = security.to_json()

    return HttpResponse(security_json)

def gannDateForecast1(request, pivotTimestamp):
    pivot1Date = np.datetime64(pivotTimestamp)
    print('DATE: ', pivot1Date) #currently timestamp is date

    maxDate = pivot1Date + np.timedelta64(1500, 'D')
    gannDates = gannSquare.getDate_all(pivot1Date, maxDate)

    gannDates_json = json.dumps(gannDates)

    return HttpResponse(gannDates_json)
def index(request):
    return HttpResponse('Security')
# Create your views here.
# ce28qc2ad3idecbgr98g