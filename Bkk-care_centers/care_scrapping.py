from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config
import care_functions

mycol = mongo_config.connection_mongo()
driver = driver_config.configure_driver()
url = "https://pflegefinder.bkk-dachverband.de/pflegedienste/searchresult.php?searchdata%5BmaxDistance%5D=0"
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

    else:
        break
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
res = {}
table = soup.find("tbody")

tr = table.findAll("tr")
for r in tr:
    res = care_functions.info_extraction(r)

    link = r.find("a", href=True)
    true_link = "https://pflegefinder.bkk-dachverband.de" + link['href']
    print(true_link)
    driver.get(true_link)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.findAll("div", {"class": "col-sm-6 col-xs12"})

    website = "N/A"
    identification_number = "N/A"

    res = care_functions.deep_info_extraction(content, res)
    final_output = mongo_config.insert_mongo(res, mycol)
    print(final_output)
driver.quit()
