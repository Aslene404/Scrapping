import json
import random
from bs4 import BeautifulSoup
import time
import driver_config
import mongo_config_C
mycol = mongo_config_C.connection_mongo()
driver = driver_config.configure_driver()
url = "https://pflegefinder.bkk-dachverband.de/aua/searchresult.php?searchdata%5Brequired%5D=1&searchdata%5Boffer_name%5D=&searchdata%5Bzip%5D=&searchdata%5Blocation%5D=&searchdata%5Bmaxdistance%5D=5&searchdata%5Btarget_group%5D=&searchdata%5Bage_group%5D=&searchdata%5Blanguage%5D=&searchdata%5Bsort%5D=distance_asc&searchdata%5Brecord_offset%5D=0"
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
table = soup.find("tbody",{"id": "search_result_table_body"})
name="N/A"
street="N/A"
house_number="N/A"
phone="N/A"
fax="N/A"
mail="N/A"
website = "N/A"
identification_number = "N/A"
number_of_beds="N/A"
number_short_time_care="N/A"
number_single_room="N/A"
number_double_room = "N/A"
contact_person_fname=""
contact_person_lname="N/A"
contact_person_salutation = "N/A"

tr = table.findAll("tr")
for r in tr:
    name = r.findAll("strong")[1].get_text()
    print(name)
    fake_address=r.find("i",{"class":"fas fa-map-marker"})
    if fake_address!=None:
        address=fake_address.next_sibling.strip()
        if address=="Ort jährlich wechselnd":
            street="Ort jährlich wechselnd"
            house_number="Ort jährlich wechselnd"
        else:
            street=r.findAll("strong")[2].next_sibling.strip().replace("- ","").split(",")[0].strip()
            house_number=r.findAll("strong")[2].next_sibling.strip().replace("- ", "").split(",")[1].strip()
    print(street)
    print(house_number)

    link = r.find("a", {"style" : "color:inherit"} ,href=True)
    true_link = "https://pflegefinder.bkk-dachverband.de/aua/" + link['href']
    print(true_link)
    driver.get(true_link)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.findAll("div", {"id": "maincontent"})
    for c in content:
        info=c.find("div",{"class","col-sm-12 col-xs-12"})
        fake_phone=info.find("i",{"class","fas fa-phone"})
        if fake_phone == None:
            phone = "N/A"
        else:
            phone = fake_phone.next_sibling.strip().replace("Telefon: ", "")

        if phone == "-":
            phone = "N/A"
        print(phone)

        fake_fax = info.find("i", {"class", "fas fa-fax"})
        if fake_fax == None:
            fax = "N/A"
        else:
            fax = fake_fax.next_sibling.strip().replace("Telefax: ", "")

        if fax == "-":
            fax = "N/A"
        print(fax)

        fake_mail = info.find("a")


        if fake_mail != None:
            mail=fake_mail.get_text().strip().replace(" ", "")
        if mail == "-":
            mail = "N/A"
        print(mail)
        fake_website=info.find("i", {"class", "fas fa-globe"})
        if fake_website!=None:

            website=fake_website.next_sibling.next_sibling.get_text()
        print(website)
        res = {'name': name,
               'street': street,
               'house_number': house_number,
               'phone': [phone],
               'fax': fax,
               'mail': mail,
               'website': website,
               'identification_number': identification_number,
               'branche': 'health',
               'category': 'care',
               'number_of_beds': number_of_beds,
               'number_short_time_care': number_short_time_care,
               'number_single_room': number_single_room,
               'number_double_room': number_double_room,
               'contact_person_fname': contact_person_fname,
               'contact_person_lname': contact_person_lname,
               'contact_person_salutation': contact_person_salutation
               }
        final_string = json.dumps(res)
        print(final_string)
        file_data = json.loads(final_string)
        print(file_data)
        xs = mycol.insert_one(file_data)
        print("Successfully inserted into mongo database with id " + str(xs.inserted_id))
driver.quit()









