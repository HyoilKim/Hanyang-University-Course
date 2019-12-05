import json
import requests
from pprint import pprint

def test1():
    print("test")

def hosp_list(lat, lng):
    lat = round(lat, 7)
    lng = round(lng, 7)
    print("@@@@@@@@@@@@@@")
    print(lat)
    print(lng)
    url = "http://apis.data.go.kr/B551182/hospInfoService/getHospBasisList"
    default_key = "3wlHL6g1M3i2oO2cnR44opHmafh54ifadIuEPG/oNu09j7iaYXKYs87dgFRZDsxfSWwzzJoVgqRhKyLHUIl96A=="
    params = {
      'pageNo': 1,  
      'numOfRows': 20,              # 가져오는 데이터 개수
      'clCd': 11,                   # 옵션(종합병원)
      'ServiceKey': default_key,    # 발급키
      'xPos': lng, #127.0331892,    # 파라미터로 받아오거나 한양대 위도,경도로 설정
      'yPos': lat, #37.5585146,
      'radius': 5000,               # 위도,경도 중심으로 ?m 까지
      '_type': 'json'               
      
    }
    pprint(params)
    r = requests.get(url, params=params)    # url에 parm정보추가
    pprint(r)
    return r.json()                         # josn 형태로 return
   
if __name__ == ("__main__"):
    lat=37.5585146
    lng=127.0331892
    
    pprint(hosp_list(lat,lng))