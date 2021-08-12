import json
from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config_H

mycol = mongo_config_H.connection_mongo()
driver = driver_config.configure_driver()

url = "https://klinikfinder.bkk-dachverband.de/suche/suchergebnis.php?searchdata%5Bplzort%5D=Berlin&searchdata%5Blocation%5D=6701%7CAGS&searchdata%5Bmaxdistance%5D=bundesweit&searchcontrol%5Blimit_offset%5D=60&searchcontrol%5Blimit_num%5D=30&searchcontrol%5Border%5D=name"
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
table = soup.find("table")

tr = table.findAll("tr")
for r in tr:
    link = r.find("a", {"class": "main-link"}, href=True)
    print(link['href'])
    driver.get(link['href'])
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    content = soup.findAll("div", {"class": "row rowtable-data"})

    for c in content:
        info = c.findAll("div", {"class": "col-sm-12"})
        for i in info:
            name = i.find("strong").get_text()
            print(name)
            street = i.findAll("br")[0].next_sibling.strip()
            print(street)
            city = i.findAll("br")[1].next_sibling.strip()
            print(city)
            phone = i.findAll("br")[2].next_sibling.strip().replace("Telefon: ", "")
            if phone == "":
                phone = "N/A"
            print(phone)
            website = i.find("a")['href']
            if website[0] != "h":
                website = "N/A"
            print(website)
    bed_link = link['href'].replace("uebersicht", "stationaere-behandlung")

    driver.get(bed_link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    bed_numbers = soup.findAll("div", {"class": "col-sm-4 col-xs-12 rowtable-title hyphenate"})
    number_of_beds = bed_numbers[1].get_text().strip()
    number_of_annual_cases = bed_numbers[3].get_text().strip()
    res = {
        'name': name,
        'street': street,
        'city': city,
        'branche':'health',
        'category':'clinics',
        'phone': [phone],
        'website': website,
        'number_of_beds': number_of_beds,
        'number_of_annual_cases': number_of_annual_cases}
    final_string = json.dumps(res)
    file_data = json.loads(final_string)
    xs = mycol.insert_one(file_data)
    print("Successfully inserted into mongo database with id " + str(xs.inserted_id))
driver.quit()
