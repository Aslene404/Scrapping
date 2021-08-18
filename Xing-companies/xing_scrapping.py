import json
import random
from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config
mycol = mongo_config.connection_mongo()
driver = driver_config.configure_driver()
url = "https://login.xing.com/?dest_url=https%3A%2F%2Fwww.xing.com%2Fsearch%2Fcompanies"
driver.get(url)
time.sleep(3)
cookies_button = driver.find_element_by_id("consent-accept-button")
if cookies_button.is_displayed():
    driver.execute_script("arguments[0].click();", cookies_button)
    time.sleep(2)
username="aslenerazor@gmail.com"
password="shadow11820977"
driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_css_selector(".fYOVsO").click()
time.sleep(3)
location_id=""
keyword="ion2s"
url="https://www.xing.com/search/companies?filter.location%5B%5D="+location_id+"&keywords="+keyword
driver.get(url)
time.sleep(1)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
res = {}


table = soup.find("div",{"role":"list"})

tr = table.findAll("div",{"class":"search-card-style-container-69860b53"})
if len(tr)==1:
    for r in tr:
        name=tr.find("div",{"class":"search-card-style-content-20754fd7"}).findAll("div")[0]

"""for r in tr:

    link = r.find("a", href=True)
    true_link = "https://www.xing.com" + link['href']

    urls.append(true_link)
for slru in urls:
    links=[]
    driver.get(slru)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.findAll("div", {"id": "listing-container"})
    for c in content:
        articles=c.findAll("article", {"class":"company-item media-10"})
        for a in articles:
            company_link=a.find("a", href=True)

            links.append("https://www.xing.com"+company_link['href'])
        for lk in links :
            name="N/A"
            ort="N/A"
            bundesland="N/A"
            user="N/A"
            range="N/A"

            driver.get(lk)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            fake_name=soup.find("h1",{"class":"herostyles__Hero-wnpgbw-0 gtwWf header-Header-title-b3386c2f"})
            if fake_name!=None:
                name=fake_name.get_text().strip()
            print(name)
            fake_address=soup.find("p",{"class":"body-copystyles__BodyCopy-x85e3j-0 loRlFk locations-Location-address-8136611d"})
            if fake_address!=None:
                ort=fake_address.get_text().strip().split(",")[0].strip()
                bundesland=fake_address.get_text().strip().split(",")[1].strip()
            print(ort)
            print(bundesland)"""





