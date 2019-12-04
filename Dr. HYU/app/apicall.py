import json
import requests
from pprint import pprint

def test1():
    print("test")

def hosp_list(lat=37.5585146, lng=127.0331892):    
    url = "http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList"
    default_key = "3wlHL6g1M3i2oO2cnR44opHmafh54ifadIuEPG/oNu09j7iaYXKYs87dgFRZDsxfSWwzzJoVgqRhKyLHUIl96A=="
    params = {
      'pageNo': 1,
      'numOfRows': 10,
      'clCd': 11,
      'ServiceKey': default_key,
      'xPos': lng, #127.0331892,
      'yPos': lat, #37.5585146,
      'radius': 5000,  
      '_type': 'json'
      
    }
    r = requests.get(url, params=params)
    return r.json()
   
if __name__ == ("__main__"):
    pprint(hosp_list())