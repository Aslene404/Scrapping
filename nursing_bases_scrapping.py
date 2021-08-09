import json
import random
from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config_C
mycol = mongo_config_C.connection_mongo()
driver = driver_config.configure_driver()
url = "https://pflegefinder.bkk-dachverband.de/suche/searchresult.php?searchdata%5Bkeyword%5D=&searchdata%5Bzip%5D=&searchdata%5Blocation%5D=&searchdata%5BmaxDistance%5D=0&searchdata%5Btype%5D%5B%5D=nursing_service&searchdata%5Btype%5D%5B%5D=nursing_home&searchdata%5Btype%5D%5B%5D=aua&searchdata%5Btype%5D%5B%5D=nursing_care_base"
driver.get(url)
time.sleep(1)
cookies_button = driver.find_element_by_id("mkc-btn-select")
if cookies_button.is_displayed():
    driver.execute_script("arguments[0].click();", cookies_button)
    time.sleep(1)
"""z = 0
while z != -1:

    more_button = driver.find_element_by_id("more_btn")
    if more_button.is_displayed():
        driver.execute_script("arguments[0].click();", more_button)

    else:
        break"""
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
res = {}
table = soup.find("tbody")

tr = table.findAll("tr")
for r in tr:
    collegues = []
    link = r.find("a", href=True)
    true_link = "https://pflegefinder.bkk-dachverband.de/" + link['href']
    print(true_link)
    driver.get(true_link)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.findAll("div", {"id": "maincontent"})
    for c in content:
        name = c.find("h1").get_text()
        print(name)
        info = c.findAll("div", {"class": "row rowtable-data"})[0].find("div")




        """if fake_address[0:22]=="Ort jährlich wechselnd" :
            street="N/A"
            print(street)
            house_number="N/A"
            print(house_number)
        else :
            address=info[0].findAll("p")
            street=address[0].findAll("br")[0].next_sibling.strip()
            print(street)"""





