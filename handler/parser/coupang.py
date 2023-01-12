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

load_dotenv()

# 검색 URL
SEARCH_URL = "https://www.coupang.com/np/search?q="

# 물건 검색 후 리스트 리턴 
def search_item(item: str) -> list[tuple]:
    driver.get("{}{}".format(SEARCH_URL, item))

    ul = driver.find_element(by=By.CLASS_NAME, value="search-product-list")
    list = ul.find_elements(by=By.TAG_NAME, value="li")

    result = []
    for i in list:
        id = i.get_attribute("id")
        detailId = i.get_attribute("data-vendor-item-id")
        name = i.find_element(by=By.CLASS_NAME, value="name").text
        price = i.find_element(by=By.CLASS_NAME, value="price-value").text.replace(",","")
        result.append((id, detailId, name, price))
        
    return result


# 상세 아이템 리스트 검색 (가격 변동 확인)
# 가격, 세일유무, 세일퍼센트
def searchDetailItem(id, detail_id) -> tuple:
    url = "https://www.coupang.com/vp/products/{}?vendorItemId={}".format(id, detail_id)
    driver.get(url)

    isSale = False
    cardSale = ""
    try:
        cardSale = driver.find_element(by=By.CLASS_NAME, value="ccid-txt").text
        isSale = True
    except Exception as e:
        pass
    
    price = driver.find_element(by=By.CLASS_NAME, value="total-price").find_element(by=By.TAG_NAME, value="strong").text
    return (price, isSale, cardSale)