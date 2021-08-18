import json

from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config
import support_functions
mycol = mongo_config.connection_mongo()
driver = driver_config.configure_driver()
url = "https://pflegefinder.bkk-dachverband.de/aua/searchresult.php?searchdata%5Brequired%5D=1&searchdata%5Boffer_name%5D=&searchdata%5Bzip%5D=&searchdata%5Blocation%5D=&searchdata%5Bmaxdistance%5D=5&searchdata%5Btarget_group%5D=&searchdata%5Bage_group%5D=&searchdata%5Blanguage%5D=&searchdata%5Bsort%5D=distance_asc&searchdata%5Brecord_offset%5D=0"
driver.get(url)
time.sleep(1)
cookies_button = driver.find_element_by_id("mkc-btn-select")
if cookies_button.is_displayed():
    driver.execute_script("arguments[0].click();", cookies_button)
    time.sleep(2)
z = 0
"""while z != -1:

    more_button = driver.find_element_by_id("more_btn")

    if more_button.is_displayed():
        driver.execute_script("arguments[0].click();", more_button)
        time.sleep(1)

    else:
        break"""
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
res = {}
table = soup.find("tbody",{"id": "search_result_table_body"})



tr = table.findAll("tr")
for r in tr:
    res=support_functions.info_extraction(r,res)

    link = r.find("a", {"style" : "color:inherit"} ,href=True)
    true_link = "https://pflegefinder.bkk-dachverband.de/aua/" + link['href']
    print(true_link)
    driver.get(true_link)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.findAll("div", {"id": "maincontent"})
    for c in content:
        res=support_functions.deep_info_extraction(c,res)

        final_output = mongo_config.insert_mongo(res, mycol)
        print(final_output)
driver.quit()









