import json

from bs4 import BeautifulSoup
import time
import driver_config
import connection_db
import nursing_bases_functions

def scrape():
    driver = driver_config.configure_driver()
    zone=["Baden-Württemberg","Bayern","Berlin","Brandenburg","Bremen","Hamburg","Hessen","Mecklenburg-Vorpommern","Niedersachsen","Nordrhein-Westfalen","Rheinland-Pfalz","Saarland","Schleswig-Holstein"]
    for zon in zone :
        z = 1
        while z != -1:
            url = "https://pflegefinder.bkk-dachverband.de/pflegeberatung/pflegestuetzpunkte/suche.php?searchcontrol%5Bsubmit%5D=1&searchdata%5Bplzort%5D=&searchdata%5Blocation%5D=&searchdata%5Bmaxdistance%5D=20&searchdata%5Bbundesland%5D="+zon+"&p="+str(z)
            z+=1
            driver.get(url)
            time.sleep(1)
            cookies_button = driver.find_element_by_id("mkc-btn-select")
            if cookies_button.is_displayed():
                driver.execute_script("arguments[0].click();", cookies_button)
                time.sleep(2)

            more_button = driver.find_elements_by_link_text('›')
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            res = {}
            table = soup.find("table", {"class": "table table-striped"}).find("tbody")
            name = "N/A"
            street = "N/A"
            house_number = "N/A"
            phone = "N/A"
            fax = "N/A"
            mail = "N/A"
            website = "N/A"
            identification_number = "N/A"
            number_of_beds = "N/A"
            number_short_time_care = "N/A"
            number_single_room = "N/A"
            number_double_room = "N/A"
            contact_person_fname = ""
            contact_person_lname = "N/A"
            contact_person_salutation = "N/A"

            tr = table.findAll("tr")
            for r in tr:
                """extracting name"""
                fake_name=r.find('a')
                if fake_name==None:
                    continue
                else:
                    name=fake_name.get_text()
                print(name)
                """extracting street and house number"""
                fake_address = r.find("i", {"class": "fas fa-map-marker"})
                if fake_address != None:
                    address = fake_address.next_sibling.strip()
                    if address == "Ort jährlich wechselnd":
                        street = "Ort jährlich wechselnd"
                        house_number = "Ort jährlich wechselnd"
                    else:
                        street = r.find("strong").next_sibling.strip().replace("- ", "").split(",")[0].strip()
                        house_number = r.find("strong").next_sibling.strip().replace("- ", "").split(",")[1].strip()
                print(street)
                print(house_number)
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
                """redirecting to nurse_base url"""
                link = r.find("a", {"style": "color:inherit"}, href=True)
                true_link = "https://pflegefinder.bkk-dachverband.de/pflegeberatung/pflegestuetzpunkte/" + link['href']
                print(true_link)
                driver.get(true_link)


                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                content = soup.findAll("div", {"id": "col-landscape"})
                for c in content:
                    res= nursing_bases_functions.deep_info_extraction(c, res)

                    final_string = json.dumps(res)
                    print(final_string)
                    file_data = json.loads(final_string)
                    print(file_data)
                    final_output = connection_db.insert_new_care_center(file_data)
                    print(final_output)
            if len(more_button) == 0 and r == tr[len(tr) - 1]:
                break

    driver.quit()
    return


