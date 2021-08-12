import json
import random
from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config_C
mycol = mongo_config_C.connection_mongo()
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
    name=r.find("a").get_text()
    print(name)
    address=r.findAll("br")[0].next_sibling.get_text().strip()
    print(address)
    street=address.split(",")[0].strip()
    print(street)
    house_number=address.split(",")[1].strip()
    print(house_number)
    fake_phone=r.find("i", {"class": "fas fa-phone"})
    if fake_phone==None:
        phone="N/A"
    else:
        phone=fake_phone.next_sibling.strip().replace("Telefon: ", "")

    if phone == "-":
        phone = "N/A"
    print(phone)
    fake_fax = r.find("i", {"class": "fas fa-fax"})
    if fake_fax==None :
        fax="N/A"
    else :
        fax=fake_fax.next_sibling.strip().replace("Fax: ", "")
    if fax == "-":
        fax = "N/A"
    print(fax)
    fake_mail=r.find("div", {"style":"white-space: nowrap; max-width: 250px; text-overflow: ellipsis; overflow: hidden;"})
    if fake_mail==None :
        mail="N/A"
    else :
        mail=fake_mail.get_text().strip()
    print(mail)
    link = r.find("a", href=True)
    true_link = "https://pflegefinder.bkk-dachverband.de" + link['href']
    print(true_link)
    driver.get(true_link)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.findAll("div", {"class": "col-sm-6 col-xs12"})
    website="N/A"
    identification_number="N/A"


    for c in content:
        fake_website = c.find("a", {"target": "_blank"})

        if fake_website != None:
            website = fake_website.get_text().strip().replace(" ", "")
        if website == "-":
            website = "N/A"

        fake_identification_number = content[1].find("br")
        if fake_identification_number == None:
            identification_number == "N/A"
        else:
            identification_number = fake_identification_number.next_sibling.strip()

    print(website)
    print(identification_number)
    res={'name':name,
         'street':street,
         'house_number':house_number,
         'phone':[phone],
         'fax':fax,
         'mail':mail,
         'website':website,
         'identification_number':identification_number,
         'branche': 'health',
         'category': 'care',
         'number_of_beds':'N/A',
         'number_short_time_care': 'N/A',
         'number_single_room': 'N/A',
         'number_double_room': 'N/A',
         'contact_person_fname': 'N/A',
         'contact_person_lname': 'N/A',
         'contact_person_salutation': 'N/A'
         }
    final_string = json.dumps(res)
    print(final_string)
    file_data = json.loads(final_string)
    print(file_data)
    xs = mycol.insert_one(file_data)
    print("Successfully inserted into mongo database with id " + str(xs.inserted_id))
driver.quit()













