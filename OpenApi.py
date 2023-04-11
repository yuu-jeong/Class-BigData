import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

ServiceKey = "wqQCYzajuadme0LeIF2Xzklvbly2FzOvEe53%2FtAKE9uyfqPvIYrWz9kklzpPHQJPYn3SyTHLUQUkI0hVwPnVnw%3D%3D"

#CODE 1
def getRequestUrl(url):
  # 매개변수로 받은 url에 대한 요청을 보낼 객체를 생성
  req = urllib.request.Request(url)
  try:
    response = urllib.request.urlopen(req)
    if response.getcode() == 200: # 요청 성공 
      print("[%s] URL Request Success" % datetime.datetime.now())
      return response.read().decode('urf-8') #디코딩하여 반환 
  except Exception as e: # 요청 실패 
    print(e)
    print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
    return None

#CODE 2
def getTourismStatsItem(yyyymm, national_code, ed_cd): #요청을 위한 URL 구성성
  service_url = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"
  parameters = "?_type=json&serviceKey=" + ServiceKey 
  parameters += "&YM=" + yyyymm
  parameters += "&NAT_CD=" + national_code
  parameters += "&ED_CD=" + ed_cd

  url = service_url + parameters
  print(url) #액세스 거부 여부 확인용
  retData = getRequestUrl(url) #[CODE 1]

  if (retData == None):
    return None
  else:
    # response가 None이 아닐 경우 json 형태의 파일을 python 객체로 변경
    return json.loads(retData)

#CODE 3
def getTourismStateService(nat_cd, ed_cd, nStartYear, nEndYear):
  jsonResult = []
  result = []
  natName=''
  dataEND = "{0}{1:0>2}".format(str(nEndYear), str(12))
  ed = ''
  isDataEnd = 0

  for year in range(nStartYear, nEndYear+1):
    for month in range(1, 13):
      if(isDataEnd == 1): break
      yyyymm = "{0}{1:0>2}".format(str(year), str(month))
      jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd) #CODE 2로 이동

      if (jsonData['response']['header']['resultMsg'] == 'OK'):  
        #데이터가 없는 마지막 항목인 경우
        if jsonData['response']['body']['items'] == '':
          isDataEnd = 1
          dataEND = "{0}{1:0>2}".format(str(year), str(month-1))
          print("데이터 없음.... \n 제공되는 통계 데이터는 %s년 %s월까지입니다." %(str(year), str(month-1)))
          break

      #jsonData를 출력하여 확인
      print(json.dumps(jsonData, indent = 4, sort_keys = True, ensure_ascii = False))
      natName = jsonData['response']['body']['items']['item']['natKorNm']
      natName = natName.replace('','' )
      num = jsonData['response']['body']['items']['item']['num']
      ed = jsonData['response']['body']['items']['item']['ed']
      print('[ %s_%s : %s ]' %(natName, yyyymm, num))
      print('--------------------------------------')
      jsonResult.append({'nat_name': natName, 'nat_cd':nat_cd, 'yyyymm': yyyymm, 'visit_cnt': num})
      result.append([natName, nat_cd, yyyymm, num])
  return(jsonResult, result, natName, ed, dataEND)

#CODE 0
def main():
  jsonResult=[]
  result=[]
  
  # 데이터를 수집할 국가 코드, 시작 연도, 마지막 연도 입력력
  print("<< 국내 입국한 외국인의 통계 데이터 수집 >>")
  nat_cd = input("국가 코드를 입력하세요(중국: 112 / 일본: 130 / 미국: 275 : ")
  nStartYear = int(input("데이터를 몇 년부터 수집할까요? : "))
  nEndYear = int(input("데이터를 몇 년까지 수집할까요? : "))
  ed_cd = "E" # 방한외래관광객

  #getTourismStatsService() 함수를 호출하여 반환받은 데이터 저장
  jsonResult, result, natName, ed, dataEND = getTourismStateService(nat_cd, ed_cd, nStartYear, nEndYear)

  if(natName =='') :
    print("데이터가 전달되지 않았습니다")

  else:
    # 파일 저장 : 파이썬 딕셔너리 -> JSON 파일
    with open('./%s_%s_%d_%s.json' % (natName, ed, nStartYear, dataEND), 'w', encoding = 'utf8') as outfile:
      jsonFile = json.dumps(jsonResult, indent = 4, sort_keys = True, ensure_ascii = False)
      outfile.write(jsonFile)
    
    # 파일 저장 : CSV 파일
    columns = ["입국자국가", "국가코드", "입국연월", "입국자 수"]
    result_df = pd.DataFrame(result, columns = columns)
    result_df.to_csv('./%s_%s_%d_%s.csv' % (natName, ed, nStartYear, dataEND), index=False, encoding='cp949')

if __name__ == '__main__':
  main()
