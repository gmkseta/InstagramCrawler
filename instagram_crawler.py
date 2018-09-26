from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get('http://www.instagram.net/tags/경복궁/')
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
# instagram_img_info={'img_url''img_src':'','tag':'','next_img_src':'','location':''}
new_url = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[2]/a').click()

img = driver.find_elements_by_css_selector(
    'body > div:nth-child(15) > div > div.zZYga > div > article > div._97aPb > div > div > div.KL4Bh > img')
img_src = [i.get_attribute('src')for i in img]
print(img_src)
location = driver.find_elements_by_css_selector(
    'body > div:nth-child(15) > div > div.zZYga > div > article > header > div.o-MQd > div.M30cS > a')
if location:
    for site in location:
        print(site.text)
else:
    print('no location data')
tag = driver.find_elements_by_css_selector(
    'body > div:nth-child(15) > div > div.zZYga > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li:nth-child(1) > div > div > div > span > a')
for t in tag:
    tags = t.text
    print(tags)

# 다음 게시글로 넘어가는 버튼
# body > div:nth-child(15) > div > div.EfHg9 > div > div > a.HBoOv.coreSpriteRightPaginationArrow
# 다음 사진으로 넘어가는 버튼
# body > div:nth-child(15) > div > div.zZYga > div > article > div._97aPb > div > div > div > div.tN4sQ.zRsZI > button > div

next_article_btn = None
next_pic_btn = None

driver.implicitly_wait(3)

next_article_btn = driver.find_element_by_link_text('다음')
next_pic_btn=driver.find_element_by_class_name('coreSpriteRightChevron')

if not next_pic_btn:
    next_article_btn.click()
else:
    next_pic_btn.click()
    driver.implicitly_wait(3)
    print('다음 사진 클릭')

# if next_img_button:
#     next_img_button.click()
#     next_img = driver.find_element_by_tag_name("img")
#     next_img_src = next_img.get_attribute('src')
#     print(next_img_src)
# else:
#     print(0)
