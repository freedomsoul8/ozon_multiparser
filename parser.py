import time
import re
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.app.data_handler import data_handler


driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), headless=False, use_subprocess=True)

def parse_url(quantity: int, input_filename: str, column_name: str):
    barcodes = data_handler.read_input_column(input_filename, column_name)
    url = []
    c = 0
    for code in barcodes:
        if c < quantity:
            driver.get(f"https://www.ozon.ru/search/?text={code}")
            time.sleep(5)
            try:
                href = driver.find_element(by=By.XPATH,value="/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[3]/div/div/div/div[1]/div/div[1]/a").get_attribute("href")
                url.append(href)
            except:
                url.append(f"404 NO PRODUCTS WITH MODEL NO {code}")
            c = c + 1
        else:
            break
    return url


def parse_item(url, item_count):
    if "404 NO" in url:
        pass
    else:
        try:
            img_links = []
            chars_title = []
            chars_data = []
            imgs = []

            img_count = 0

            driver.get(url)
            if item_count == 0 or 1:
                time.sleep(5)
            else:
                pass
            time.sleep(2)

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            title = soup.find("div", {"data-widget":"webProductHeading"}).text
            ct = soup.find("div", {"id": "section-characteristics"}).find_all("dt")
            cd = soup.find("div", {"id": "section-characteristics"}).find_all("dd")
            for i in ct:
                chars_title.append(i.text)
            for s in cd:
                chars_data.append(s.text)
            price = soup.find("div", {"data-widget": "webPrice"}).text
            breadcrumbs = re.findall(r"[A-ZА-Я]?[^A-ZА-Я]*",soup.find("div", {"data-widget": "breadCrumbs"}).text)
            breadcrumb_data = soup.find("div", {"data-widget": "breadCrumbs"}).text
            if breadcrumb_data in data_handler.breadcrumbs:
                pass
            else:
                data_handler.breadcrumbs.append(breadcrumb_data)
            img_container = soup.find("div", {"data-widget": "webGallery"}).find_all("img")
            try:
                sku = soup.find("span",{"data-widget":"webDetailSKU"}).text
            except:
                sku = soup.find("div", {"data-widget": "webDetailSKU"}).text
            for img in img_container:
                img_links.append(img["src"].replace("/wc50", "/wc1000"))
            for img_href in img_links:
                img_get = requests.get(img_href)
                with open(f"imgs/{sku.replace('Код товара: ', '')}_{img_count}.jpg", "wb") as img_file:
                    imgs.append(f"{sku.replace('Код товара: ', '')}_{img_count}.jpg")
                    img_file.write(img_get.content)
                    img_count += 1

            data_handler.container.append([title, "".join(breadcrumbs[-3:len(breadcrumbs)-2]), sku.replace("Код товара: ", ""), imgs, chars_title, chars_data])
            print(item_count,[title, "".join(breadcrumbs[-3:len(breadcrumbs)-2]), sku.replace("Код товара: ", ""), imgs, chars_title, chars_data])
        except Exception as e:
            print(item_count,f"[{e}]")
            pass




# data_handler.export_urls(filename="750_MN.xlsx",urls=parse_url(quantity=750,input_filename="input.xlsx",column_name="MODEL NO"))
urls = data_handler.read_input_column(filename=r"750_MN.xlsx",column_name="url")

for url in urls:
    parse_item(url, urls.index(url))

data_handler.create_excel_table(data_handler.container)
data_handler.new_breadcrumbs(breadcrumbs_list=data_handler.breadcrumbs)