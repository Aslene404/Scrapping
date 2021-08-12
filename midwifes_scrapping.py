import json

from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config_MW

mycol = mongo_config_MW.connection_mongo()
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
        name_ex = d.findAll("strong")
        for n in name_ex:
            name = n.get_text()
            print(name)



            first_name = name.split()[0]
            print(first_name)
            last_name = name.split(' ', 1)[1]
            print(last_name)


            phone_mail = d.findAll("a")
            if len(phone_mail) == 2:
                phone = phone_mail[0].get_text().strip().replace("Telefon: ", "")
                mail = phone_mail[1].get_text().strip().replace("E-Mail: ", "")
            if len(phone_mail) == 1:
                phone = phone_mail[0].get_text().strip().replace("Telefon: ", "")
                mail = "N/A"
            if len(phone_mail) == 0:
                phone = "N/A"
                mail = "N/A"

            print(phone)

            print(mail)
            res = {
                'branche':'health',
                'category': 'midwife',
                'salutation': 'Frau',
                'first_name': first_name,
                'last_name': last_name,
                'phone': [phone],
                'mail': mail
            }

        serv = d.findAll("span", {"class": "sr-only"})

        for s in serv:

            if s.get_text() == ": Ja":
                data.append(True)
            else:
                data.append(False)
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
        xs = mycol.insert_one(file_data)
        print("Successfully inserted into mongo database with id " + str(xs.inserted_id))
driver.quit()
