from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import logging
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Driver option
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

# 셀레니움 4.0 대응으로 드라이버 호출 방법 변경
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chrome_options)
driver2 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chrome_options)

load_dotenv()


# 게시판 진입 (비어있는 곳 찾기)
def parse_html_with_url(url: str):
    logging.info("parse start")
    items = ""
    for i in range(1,6):
        try:
            driver.get("{}{}".format(url,str(i)))

            ul = driver.find_element(by=By.CLASS_NAME, value='page-list')
            li = ul.find_elements(by=By.TAG_NAME, value="li")

            for row in li:
                r = row.find_element(by=By.CSS_SELECTOR, value="div.flex-grow.truncate > a").text
                href = row.find_element(by=By.CSS_SELECTOR, value="div.flex-grow.truncate > a").get_attribute("href")
                magnet = get_magnet(href=href)

                items += """
                    <item>
                        <title>{}</title>
                        <link>{}</link>
                        <description>
                            
                        </description>
                    </item>
                """.format(r, magnet)
        except:
            logging.error("Error :: 사이트 주소 또는 파싱 에러")
            return

    if(items != ""):
        file_name = ""
        if(url == os.environ.get("DRAMA")):
            file_name = "example"
        elif(url == os.environ.get("MOVIE")):
            file_name = "example2"
        elif(url == os.environ.get("ANI")):
            file_name = "example3"
            
        make_rss(add_line=items, file_name=file_name)
    logging.info("rss make done")


def get_magnet(href: str)-> str:
    driver2.get(href)
    return driver2.find_element(by=By.CSS_SELECTOR, value="body > div.container.mx-auto.max-w-7xl.flex.flex-col.lg\:flex-row.pb-4.mt-2.text-sm > div.flex-grow > div.w-full > div.mt-2 > div.border.p-2 > div.box_content.p-0 > div:nth-child(6) > div > a.ml-2.p-2.border.text-16px").get_attribute("href")


def make_rss(add_line: str, file_name: str):
    # 경로는 맞게 수정 필요 (리눅스 도커 맵핑 기준)
    ff= open("../rss/{}.xml".format(file_name), "w+")
    with open("/home/rss_template.xml", "r+") as f:
        lines = ""
        for line in f:
            if(line.startswith("        {__수정할부분__}")):
                lines += add_line
            else:
                lines += line
        ff.write(lines)
    ff.close()


def call_all_rss():
    parse_html_with_url(url=os.environ.get("DRAMA"))
    parse_html_with_url(url=os.environ.get("MOVIE"))
    parse_html_with_url(url=os.environ.get("ANI"))
    driver.quit()
    driver2.quit()


if (__name__ == "__main__"):
    """init function"""
    logging.info("Start main function")
    call_all_rss()