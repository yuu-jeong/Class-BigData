import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

from matplotlib import font_manager, rc
font_path="C:\Windows\Fonts\\batang.ttc"
font=font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

ServiceKey="wqQCYzajuadme0LeIF2Xzklvbly2FzOvEe53%2FtAKE9uyfqPvIYrWz9kklzpPHQJPYn3SyTHLUQUkI0hVwPnVnw%3D%3D"

#[CODE 1]
def getRequestUrl(url):    
    req = urllib.request.Request(url)    
    try: 
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


#[CODE 2]
def getTourismStatsItem(yyyymm, national_code, ed_cd):    
    service_url = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"
    parameters = "?_type=json&serviceKey=" + ServiceKey   #인증키
    parameters += "&YM=" + yyyymm
    parameters += "&NAT_CD=" + national_code
    parameters += "&ED_CD=" + ed_cd
    url = service_url + parameters
    
    retData = getRequestUrl(url)   #[CODE 1]
    
    if (retData == None):
        return None
    else:
         return json.loads(retData)

#[CODE 3]
def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []
    result = []
    natName=''
    dataEND = "{0}{1:0>2}".format(str(nEndYear), str(12)) #데이터 끝 초기화
    isDataEnd = 0 #데이터 끝 확인용 flag 초기화
    ed=''
    
    for year in range(nStartYear, nEndYear+1):        
        for month in range(1, 13):
            if(isDataEnd == 1): break #데이터 끝 flag 설정되어있으면 작업 중지.
            yyyymm = "{0}{1:0>2}".format(str(year), str(month))            
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd) #[CODE 2]
            
            if (jsonData['response']['header']['resultMsg'] == 'OK'):               
                # 입력된 범위까지 수집하지 않았지만, 더이상 제공되는 데이터가 없는 마지막 항목인 경우 -------------------
                if jsonData['response']['body']['items'] == '': 
                    isDataEnd = 1 #데이터 끝 flag 설정
                    dataEND = "{0}{1:0>2}".format(str(year), str(month-1))
                    print("데이터 없음.... \n제공되는 통계 데이터는 %s년 %s월까지입니다." %(str(year), str(month-1)))                    
                    break                
                #jsonData를 출력하여 확인
                         
                natName = jsonData['response']['body']['items']['item']['natKorNm']
                natName = natName.replace(' ', '')
                num = jsonData['response']['body']['items']['item']['num']
                ed = jsonData['response']['body']['items']['item']['ed']
                print('[ %s_%s : %s ]' %(natName, yyyymm, num))
                print('----------------------------------------------------------------------')                
                jsonResult.append({'nat_name': natName, 'nat_cd': nat_cd,'yyyymm': yyyymm, 'visit_cnt': num})
                result.append([natName, nat_cd, yyyymm, num])              
    return (jsonResult, result, natName, ed, dataEND)

#[CODE 0]
def main():
    jsonResult1 = []
    jsonResult2 = []
    result1 = []
    result2 = []
    natName1 = ''
    natName2 = ''
    print("<< 국내 입국한 외국인의 통계 데이터를 수집합니다. >>")
    
    nat_cd1 = input('첫번째 국가 코드를 입력하세요(중국: 112 / 일본: 130 / 미국: 275) : ')
    nat_cd2 = input('두번째 국가 코드를 입력하세요(중국: 112 / 일본: 130 / 미국: 275) : ')

    nStartYear =int(input('데이터를 몇 년부터 수집할까요? : '))
    nEndYear = int(input('데이터를 몇 년까지 수집할까요? : '))
    ed_cd = "E"     #E : 방한외래관광객, D : 해외 출국
    
    jsonResult1, result1, natName1, ed, dataEND =getTourismStatsService(nat_cd1, ed_cd, nStartYear, nEndYear) #[CODE 3]
    jsonResult2, result2, natName2, ed, dataEND =getTourismStatsService(nat_cd2, ed_cd, nStartYear, nEndYear) #[CODE 3]


    if (natName1=='') : #URL 요청은 성공하였지만, 데이터 제공이 안된 경우
        print('데이터가 전달되지 않았습니다. 공공데이터포털의 서비스 상태를 확인하기 바랍니다.')
    else:
        #파일저장 1 : json 파일
        #국가1
        with open('./%s_%s_%d_%s.json' % (natName1, ed, nStartYear, dataEND), 'w', encoding='utf8') as outfile:
            jsonFile1  = json.dumps(jsonResult1, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(jsonFile1)

        #국가2
        with open('./%s_%s_%d_%s.json' % (natName2, ed, nStartYear, dataEND), 'w', encoding='utf8') as outfile:
            jsonFile2  = json.dumps(jsonResult2, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(jsonFile2)
            
        #파일저장 2 : csv 파일
        #국가1
        columnsList = ["입국자국가", "국가코드", "입국연월", "입국자 수"]
        result_df1 = pd.DataFrame(result1, columns = columnsList)
        result_df1.to_csv('./%s_%s_%d_%s.csv' % (natName1, ed, nStartYear, dataEND),index=False, encoding='cp949')

        #국가2
        result_df2 = pd.DataFrame(result2, columns = columnsList)
        result_df2.to_csv('./%s_%s_%d_%s.csv' % (natName2, ed, nStartYear, dataEND),index=False, encoding='cp949')

        # 막대 그래프 그리기
        yyyymmList = result_df1["입국연월"].values.tolist()
 
        visitNumList1 = result_df1["입국자 수"].values.tolist()
        visitNumList2 = result_df2["입국자 수"].values.tolist()

        xlabel = np.arange(len(yyyymmList))

        plt.bar(xlabel, visitNumList1, label=natName1, color='r', width=0.2)
        plt.bar(xlabel+0.2, visitNumList2, label=natName2, color='b', width=0.2)
        plt.xticks(xlabel, yyyymmList)

        plt.legend(loc="upper right")
        plt.title("2019~2020 입국자수")
        plt.xlabel("입국연월")
        plt.ylabel("입국자 수")

        plt.show()
                  
        
if __name__ == '__main__':
    main()
