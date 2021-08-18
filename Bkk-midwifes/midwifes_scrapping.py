import json

from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config
import midwifes_functions

mycol = mongo_config.connection_mongo()
driver = driver_config.configure_driver()
url = "https://hebammenfinder.bkk-dachverband.de/suche/suchergebnis.php"
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
table = soup.find("table")

tr = table.findAll("tr")
th = table.findAll("th")
schwangerenvorsorge = False
hausgeburt = False
beleggeburt = False
geburtshausgeburt = False
wochenbettbetreuung = False
kurse = False

for r in tr:

    td = r.findAll("td")
    data = []
    for d in td:
        res=midwifes_functions.info_extraction(d,res)
        data=midwifes_functions.service_extraction(d,data)


    print(data)
    if len(data) == 8:
        schwangerenvorsorge = data[2]
        hausgeburt = data[3]
        beleggeburt = data[4]
        geburtshausgeburt = data[5]
        wochenbettbetreuung = data[6]
        kurse = data[7]
    if len(data) == 7:
        schwangerenvorsorge = data[1]
        hausgeburt = data[2]
        beleggeburt = data[3]
        geburtshausgeburt = data[4]
        wochenbettbetreuung = data[5]
        kurse = data[6]
    res["parental_care"] = schwangerenvorsorge
    res["domestic_birth"] = hausgeburt
    res["supervised_birth"] = beleggeburt
    res["birthing_center"] = geburtshausgeburt
    res["postpartum_care"] = wochenbettbetreuung
    res["courses"] = kurse
    print(res)
    specialty = [("parental_care", schwangerenvorsorge),
                 ("domestic_birth", hausgeburt),
                 ("supervised_birth", beleggeburt),
                 ("birthing_center", geburtshausgeburt),
                 ("postpartum_care", wochenbettbetreuung),
                 ("courses", kurse)
                 ]
    res["specialty"] = specialty
    final_string = json.dumps(res)
    file_data = json.loads(final_string)
    if data != []:
        final_output = mongo_config.insert_mongo(res, mycol)
        print(final_output)
driver.quit()
