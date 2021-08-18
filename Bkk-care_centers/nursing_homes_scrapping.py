import json

from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config
import nursing_homes_functions
mycol = mongo_config.connection_mongo()
driver = driver_config.configure_driver()

z = 0
while z != -1:


    url = "https://pflegefinder.bkk-dachverband.de/pflegeheime/searchresult.php?searchdata%5BmaxDistance%5D=0#/limit/20/offset/"+str(z)
    z+=20
    zx=z

    driver.get(url)
    time.sleep(3)


    cookies_button = driver.find_element_by_id("mkc-btn-select")
    if cookies_button.is_displayed():
        driver.execute_script("arguments[0].click();", cookies_button)
        time.sleep(2)



    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    res = {}
    next_button=soup.findAll("a")
    for nb in next_button:
        print(nb.get_text().strip())
        if nb.get_text().strip()!="›":
            z=-1
        if nb.get_text().strip()=="›":
            z=zx
            break

    table = soup.find("table", {"id": "table-pei"}).find("tbody")


    tr = table.findAll("tr")

    for r in tr:
        res=nursing_homes_functions.info_extraction(r, res)


        link = r.find("a", href=True)
        print(link['href'])
        driver.get(link['href'])


        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.findAll("div", {"class": "col-sm-6 col-xs12"})





        if len(content)!=0:
            res=nursing_homes_functions.deep_info_extraction(content,res)

        final_output = mongo_config.insert_mongo(res, mycol)
        print(final_output)


driver.quit()



























