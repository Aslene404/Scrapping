import json

from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config
import mongo_config_H
import doctors_functions

mycol = mongo_config.connection_mongo()
clinics = mongo_config_H.connection_mongo()
driver = driver_config.configure_driver()
url = "https://arztfinder.bkk-dachverband.de/suche/suchergebnis.php"
driver.get(url)
time.sleep(1)
cookies_button = driver.find_element_by_id("mkc-btn-select")
if cookies_button.is_displayed():
    driver.execute_script("arguments[0].click();", cookies_button)
    time.sleep(2)
z = 0
while z != -1:

    more_button = driver.find_element_by_id("more_btn")
    if more_button.is_displayed():
        driver.execute_script("arguments[0].click();", more_button)
        time.sleep(1)
        
    else :
        break
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
res = {}
table = soup.find("tbody")
urls=[]

tr = table.findAll("tr")
for r in tr:
    collegues = []
    link = r.find("a", href=True)
    true_link = "https://arztfinder.bkk-dachverband.de/suche/" + link['href']
    print(true_link)
    urls.append(true_link)
for slru in urls :
    driver.get(slru)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.findAll("div", {"id": "maincontent"})
    for c in content:
        res=doctors_functions.deep_info_extraction(c,res,clinics,collegues)

        final_output = mongo_config.insert_mongo(res, mycol)
        print(final_output)
driver.quit()
