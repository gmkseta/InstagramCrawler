from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
from bs4 import BeautifulSoup
import pymysql
from db_env import host, user, password, db, charset

# 로딩
options = webdriver.ChromeOptions()
options.add_argument('headless')
# options.add_argument('window-size=1920*1080')
# options.add_argument("disable-gpu")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ")
driver = webdriver.Chrome('chromedriver', chrome_options=options)
driver.get('http://www.instagram.net/tags/경복궁/')
driver.implicitly_wait(3)

# SQL
insert_metadata_sql = "INSERT INTO insta_metadata(insta_location) VALUES (%s)"
insert_hashtag_sql = "INSERT INTO insta_hashtag(insta_data_id, insta_hashtag) " \
                     "VALUES ((SELECT MAX(insta_data_id) FROM insta_metadata), %s)"
insert_img_info_sql = "INSERT INTO image_info(image_url, search_keyword, img_type, insta_data_id, crawling_date)" \
                      " VALUES (%s, %s, 1, (SELECT MAX(insta_data_id) FROM insta_metadata), now())"
get_insta_id_sql = "SELECT MAX(insta_data_id) FROM insta_metadata"

# database setting
is_conn_success = False
while not is_conn_success:
    conn = None
    try:
        conn = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               db=db,
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        print("db connection exception occures")
        print(e)
        continue

    if conn is not None:
        is_conn_success = True

cursor = conn.cursor()


# functions
def extract_hash_tags(s):
    #return list(part[1:] for part in s.split() if part.startswith('#'))
    regex = r'(\#[a-zA-Z가-힣]+\b)(?!;)'
    result = re.findall(regex, s)
    result = [i.replace('#', '') for i in result]
    print('regex result : ', result)
    return result


# scroll
body = driver.find_element_by_tag_name("body")
num_of_pagedowns = 5
while num_of_pagedowns:

    num_of_pagedowns = num_of_pagedowns - 1
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
            url_list = list()
            article_url = pic.select_one('a').get('href')
            j_post_url = "https://www.instagram.com" + article_url + "&__a=1"
            print(j_post_url)
            resp = requests.get(url=j_post_url)
            data = resp.json()
            shortcode_media = data["graphql"]["shortcode_media"]
            typename = shortcode_media["__typename"]

            if typename == "GraphSidecar":
                edge_sidecar_to_children = shortcode_media["edge_sidecar_to_children"]
                nodes = edge_sidecar_to_children["edges"]
                # print("%d 개의 이미지가 있습니다." % len(nodes))
                for i in range(len(nodes)):
                    # print(nodes[i])
                    img_url = nodes[i]['node']["display_resources"][0]["src"]
                    url_list.append(img_url)
                    # print("%d 번째:" % i + img_url)
            elif typename == "GraphImage":
                img_url = shortcode_media["display_resources"][0]["src"]
                # print("1개의 이미지가 있습니다.")
                # print(img_url)
                url_list.append(img_url)
            else:
                pass

            try:
                location = shortcode_media["location"]["name"]
                print("장소 : " + location)
            except KeyError:
                location = ""
            except TypeError:
                location = ""

            caption = shortcode_media["edge_media_to_caption"]["edges"]
            hashtags = list()
            if caption == []:
                pass
            else:
                article_text = caption[0]["node"]["text"]
                hashtags = extract_hash_tags(article_text)


            data = dict()
            url_list_size = len(url_list)
            keyword_list = ["경복궁" for i in range(url_list_size)]
            data['img_url'] = [(i, j) for i, j in zip(url_list, keyword_list)]
            # data['text'] = article_text
            if hashtags:
                data['hashtags'] = hashtags
            else:
                data['hashtags'] = []
            data['location'] = location

            print(data)
            try:

                cursor.execute(insert_metadata_sql, (data['location'],))
                if data['hashtags']:
                    cursor.executemany(insert_hashtag_sql, data['hashtags'])
                # # # 나중에 경복궁 말고 다른 키워드도 들어갈 수 있게 수정할 것
                cursor.executemany(insert_img_info_sql, data['img_url'])
                # print(type(data['img_url']))
                conn.commit()
            except Exception as e:
                print(e)
                break
            finally:
                url_list = list()

cursor.close()
conn.close()
