from selenium import webdriver
import selenium.common.exceptions

#로딩
options=webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
#options.add_argument('--headless') 이거 넣으면 chrome이 안돌아가요....엉엉..
options.add_argument('window-size=1920*1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome('chromedriver',chrome_options=options)
driver.get('http://www.instagram.net/tags/경복궁/')
driver.implicitly_wait(3)

#첫 이미지 클릭
new_url = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[2]/a').click()

# 게시물 src, 위치, tag
while True:
    # img = driver.find_elements_by_css_selector(
    # 'div > div.zZYga > div > article > div._97aPb > div > div > div.KL4Bh > img')
    img = driver.find_elements_by_css_selector("div>div>div.KL4Bh > img")
    img_src = [i.get_attribute('src')for i in img]
    print(img_src)
    try:
        location = driver.find_elements_by_css_selector(
    'body > div:nth-child(15) > div > div.zZYga > div > article > header > div.o-MQd > div.M30cS > a')
    except selenium.common.exceptions.NoSuchElementException:
        location=None

    if location:
        for site in location:
            print(site.text)
    else:
        print('no location data')
    try:
        tag = driver.find_elements_by_css_selector(
    'body > div:nth-child(15) > div > div.zZYga > div > article > div.eo2As > div.KlCQn.EtaWk > ul > li:nth-child(1) > div > div > div > span > a')
    except selenium.common.exceptions.NoSuchElementException:
        tag=list()
    if tag:
        for t in tag:
            tags = t.text
            print(tags)
    else:
        print("no tags")


    while True:
    # 다음 사진 버튼, 다음 게시글 버튼
        next_article_btn = None
        next_pic_btn = None

        next_article_btn = driver.find_element_by_link_text('다음')
        try:
            next_pic_btn=driver.find_element_by_class_name('coreSpriteRightChevron')
        except selenium.common.exceptions.NoSuchElementException:
            next_pic_btn = None
            print("사진버튼 없음")

        if not next_pic_btn:
            next_article_btn.click()
            break
        else:
            next_pic_btn.click()
            driver.implicitly_wait(1)
            print('다음 사진 클릭')
            # next_img = driver.find_elements_by_css_selector("div>div>div.KL4Bh > img")
            # next_img_src = [i.get_attribute('src')for i in next_img]
            # print(next_img_src)
