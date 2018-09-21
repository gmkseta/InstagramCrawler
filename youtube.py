from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
driver=webdriver.Chrome()
driver.implicitly_wait(3)
driver.get('http://www.instagram.net/tags/경복궁/')
time.sleep(2)
body=driver.find_element_by_tag_name("body")
num_of_pagedowns=1
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.3)
def download_img_url():
    html=driver.page_source
    soup=BeautifulSoup(html,"html.parser")
    img=soup.findAll('div',attrs={'class':'KL4Bh'})
    img_src=img.get("src")

driver.close()



