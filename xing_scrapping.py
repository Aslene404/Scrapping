import json
import random
from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config_C
mycol = mongo_config_C.connection_mongo()
driver = driver_config.configure_driver()
url = "https://www.xing.com/companies/industries"
driver.get(url)
time.sleep(3)
cookies_button = driver.find_element_by_id("consent-accept-button")
if cookies_button.is_displayed():
    driver.execute_script("arguments[0].click();", cookies_button)
    time.sleep(2)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
res = {}
table = soup.find("div",{"class":"clfx foundation-row"})
urls=[]

tr = table.findAll("li")
for r in tr:

    link = r.find("a", href=True)
    true_link = "https://www.xing.com" + link['href']

    urls.append(true_link)
for slru in urls:
    links=[]
    driver.get(slru)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.findAll("div", {"id": "listing-container"})
    for c in content:
        articles=c.findAll("article", {"class":"company-item media-10"})
        for a in articles:
            company_link=a.find("a", href=True)

            links.append("https://www.xing.com"+company_link['href'])
        for lk in links :
            driver.get(lk)
            time.sleep(1)



