from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
from bs4 import BeautifulSoup
#로딩
options=webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920*1080')
# options.add_argument("disable-gpu")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ")
driver = webdriver.Chrome('chromedriver', chrome_options=options)
driver.get('http://www.instagram.net/tags/경복궁/')
driver.implicitly_wait(3)

# functions
def extract_hash_tags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))
# scroll
body = driver.find_element_by_tag_name("body")
num_of_pagedowns = 1
while num_of_pagedowns:
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    c = soup.select_one('#react-root')
    pic_line_list = c.select('div.Nnq7C')
    for pic_line in pic_line_list:
        if pic_line not in pic_line_list[-4:]:
            continue
        for pic in pic_line:
            article_url = pic.select_one('a').get('href')
            j_post_url = "https://www.instagram.com"+article_url+"&__a=1"
            print(j_post_url)
            resp=requests.get(url=j_post_url)
            data=resp.json()
            shortcode_media = data["graphql"]["shortcode_media"]
            typename=shortcode_media["__typename"]

            if typename == "GraphSidecar":
                edge_sidecar_to_children = shortcode_media["edge_sidecar_to_children"]
                nodes = edge_sidecar_to_children["edges"]
                print("%d 개의 이미지가 있습니다." % len(nodes))
                for i in range(len(nodes)):
                    print(nodes[i])
                    img_url=nodes[i]['node']["display_resources"][0]["src"]
                    print("%d 번째:" % i + img_url)
            elif typename == "GraphImage":
                img_url=shortcode_media["display_resources"][0]["src"]
                print("1개의 이미지가 있습니다.")
                print(img_url)
            else:
                pass

            try:
                location=shortcode_media["location"]["name"]
                print("장소 : "+ location)
            except KeyError:
                location=""
            except TypeError:
                location=""


            caption=shortcode_media["edge_media_to_caption"]["edges"]
            if caption == []:
                pass
            else:
                article_text = caption[0]["node"]["text"]
                hashtags = extract_hash_tags(article_text)
                print(hashtags)






