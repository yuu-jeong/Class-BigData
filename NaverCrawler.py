import os
import sys
import urllib.request
import datetime
import time
import json

# 발급받은 네이버 Client ID
client_id = 'TiN6guTVi0V5LGOk1QgZ'
client_secret = 'zwIT6_TaQy'

#[CODE 1]
#실제 HTTP 통신 실행부
def getRequestUrl(url):
    req = urllib.request.Request(url) #요청 헤더에 클라이언트 ID,Secret 추가
    req.add_header("X-Naver-Client-Id", client_id)          
    req.add_header("X-Naver-Client-Secret", client_secret)
    try:
        response = urllib.request.urlopen(req) #요청 객체 전송
        if response.getcode() == 200: #응답을 json 형태로 수신
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8') # 디코드하여 response return
    except Exception as e:
        print(e) #잘못된 쿼리 요청일 때 400 -> start 1001일 때
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#[CODE 2]
#node, 검색 대상, 시작점(1), 끝(100)
def getNaverSearch(node,srcText,start,display):
    base="https://openapi.naver.com/v1/search"
    node="/%s.json" %node
    parameters="?query=%s&start=%s&display=%s" %(urllib.parse.quote(srcText),start,display)
    url=base+node+parameters
    responseDecode=getRequestUrl(url)
    
    if(responseDecode==None):
        return None
    else:
        return json.loads(responseDecode)

#[CODE 3]
def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate=datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pDate=pDate.strftime("%Y-%m-%d %H:%M:%S")
    jsonResult.append({'cnt':cnt, 'title':title, 'description': description,
            'org_link':org_link, 'link': org_link, 'pDate':pDate})
    return

#[CODE 0]-MAIN
#셋팅 메모장으로!
def main():
    node = 'news' #크롤링 할 대상
    srcText = input("검색어를 입력하세요: ")
    cnt = 0
    jsonResult = []

    jsonResponse=getNaverSearch(node, srcText, 1, 100)
    total = jsonResponse['total']
    
    while((jsonResponse != None) and (jsonResponse['display']!=0)):
        for post in jsonResponse['items']:
            cnt+=1
            getPostData(post,jsonResult,cnt)
        
        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)

    print('전체 검색 : %d 건' %total)
    
    with open('%s_naver_%s.json' %(srcText,node), 'w', encoding='utf8') as outfile:
        jsonFile=json.dumps(jsonResult,indent=4,sort_keys=True,ensure_ascii=False)
        outfile.write(jsonFile) 

    print("가져온 데이터 : %d 건" %(cnt))
    print('%s_naver_%s.json SAVED' % (srcText, node))

if __name__ == '__main__':
    main()
