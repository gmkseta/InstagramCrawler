from bs4 import BeautifulSoup
import urllib.request
import time
import os
def get(max_count=1):
    start=time.time()
    base_url="http://10000img.com/"
    url="http://10000img.com/ran.php"

    count=1
    while count <=max_count:
        print("+----------[%d번 째 이미지 ]----------+"% count)

        html=urllib.request.urlopen(url)
        source = html.read()
        soup=BeautifulSoup(source,"html.parser")
        img=soup.find("img")
        img_src=img.get("src")
        img_url=base_url+img_src
        img_name=img_src.replace("/","")

        if not duplicate(img_name):
            urllib.request.urlretrieve(img_url,"./img/"+img_name)
        else:
            print("중복된 이미지!")
        print("이미지 src:",img_src)
        print("이미지 url:",img_url)
        print("이미지 명:",img_name)
        print("\n")
        count +=1
    else:
        print("크롤링 종료")
        print("크롤링 소요 시간:",round(time.time()-start,6))
get(25)


