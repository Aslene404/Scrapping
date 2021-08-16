import json
import random
from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config_Doc
import mongo_config_H

mycol = mongo_config_Doc.connection_mongo()
clinics = mongo_config_H.connection_mongo()
driver = driver_config.configure_driver()
url = "https://arztfinder.bkk-dachverband.de/suche/suchergebnis.php"
driver.get(url)
time.sleep(1)
cookies_button = driver.find_element_by_id("mkc-btn-select")
if cookies_button.is_displayed():
    driver.execute_script("arguments[0].click();", cookies_button)
    time.sleep(10)
z = 0
"""while z != -1:

    more_button = driver.find_element_by_id("more_btn")
    if more_button.is_displayed():
        driver.execute_script("arguments[0].click();", more_button)
        time.sleep(1)
        
    else :
        break"""
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
        name = c.find("h1").get_text()
        print(name)
        salutation = name.split()[0]
        print(salutation)
        proto = name.split(' ', 1)[1]
        print(proto)
        splits = proto.split()
        title = ""
        for split in splits:
            if len(split) == 2:
                break
            if split[len(split) - 1] == "." or split[len(split) - 1] == ")":
                title += split + " "

        print(title)
        first_last = proto.replace(title, "")
        print(first_last)
        first_name = first_last.split()[0]
        print(first_name)
        last_name = first_last.split(' ', 1)[1]
        print(last_name)
        info = c.findAll("div", {"class": "col-sm-6 col-xs-12"})

        street = info[0].findAll("br")[0].next_sibling.strip()
        print(street)
        house_number = info[0].findAll("br")[1].next_sibling.strip()
        print(house_number)
        phone = info[0].find("i", {"class": "fa fa-phone"}).next_sibling.strip().replace("Telefon: ", "")

        if phone == "":
            phone = "N/A"
        print(phone)
        fax = info[0].find("i", {"class": "fa fa-fax"}).next_sibling.strip().replace("Fax: ", "")

        if fax == "Fax:":
            fax = "N/A"
        print(fax)
        true_website="N/A"


        website = info[0].findAll("a")
        for web in website :



            true_website = web.get_text()
            print(true_website)
        health_insurance_approval = info[1].findAll("br")[0].next_sibling.strip()
        print(health_insurance_approval)
        if health_insurance_approval == "Ja":
            health_insurance_approval = True
            print(health_insurance_approval)
        if health_insurance_approval == "Nein":
            health_insurance_approval = False
            print(health_insurance_approval)
        if health_insurance_approval == "Nicht bekannt":
            health_insurance_approval = "N/A"
            print(health_insurance_approval)

        family_doctor = info[1].findAll("br")[1].next_sibling.strip()
        print(family_doctor)
        if family_doctor == "Ja":
            family_doctor = True
            print(family_doctor)
        if family_doctor == "Nein":
            family_doctor = False
            print(family_doctor)
        if family_doctor == "Nicht bekannt":
            family_doctor = "N/A"
            print(family_doctor)

        home_visits = info[1].findAll("br")[2].next_sibling.strip()
        print(home_visits)
        if home_visits == "Ja":
            home_visits = True
            print(home_visits)
        if home_visits == "Nein":
            home_visits = False
            print(home_visits)
        if home_visits == "Nicht bekannt":
            home_visits = "N/A"
            print(home_visits)
        group_practice = info[1].findAll("br")[3].next_sibling.strip()
        print(group_practice)
        if group_practice == "Ja":
            group_practice = True
            print(group_practice)

            colle = info[1].findAll("a")
            for co in colle:
                print(co.get_text().strip())
                collegues.append(co.get_text().strip())
            print(collegues)
        if group_practice == "Nein":
            group_practice = False
            print(group_practice)
        if group_practice == "Nicht bekannt":
            group_practice = "N/A"
            print(group_practice)
        spec = c.findAll("div", {"class": "row rowtable-data"})
        specialties = []
        for sp in spec:
            lis = sp.findAll("li")

            for li in lis:
                print(li.get_text().strip())
                specialties.append(li.get_text().strip())
        print(specialties)
        myclinic=""
        cli = clinics.find_one({"street": street,
                                "city": house_number})
        print(cli)
        if cli :
            myclinic = cli.name()
            print(myclinic)

        res = {
            'salutation': salutation,
            'first_name': first_name,
            'last_name': last_name,
            'street': street,
            'house_number': house_number,
            'branche': 'health',
            'category': 'doctors',
            'phone': [phone],
            'website': true_website,
            'fax': fax,
            'specialty': specialties,
            'clinic': myclinic,
            'health_insurance_approval': health_insurance_approval,
            'family_doctor': family_doctor,
            'home_visits': home_visits,
            'group_practice': group_practice,
            'collegues': collegues}

        final_string = json.dumps(res)
        print(final_string)
        file_data = json.loads(final_string)
        print(file_data)
        xs = mycol.insert_one(file_data)
        print("Successfully inserted into mongo database with id " + str(xs.inserted_id))
driver.quit()
