import json

from bs4 import BeautifulSoup
import time
import driver_config
import connection_db
import error_connection_db
import nursing_bases_functions


def scrape():
    while True:
        driver = driver_config.configure_driver()
        counter=1
        doc_order = 0
        index=0
        zone = ["Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen",
                "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland",
                "Schleswig-Holstein"]  # array containing all the bundeslands used for the filter
        inserted_documents = 0  # counter to count the number of inserted documents to the database
        try:
            primal_res = error_connection_db.is_exit_with_error()  # get the latest document inserted before the error

            if primal_res != None:
                for i in primal_res:
                    if i == "offset":
                        counter = primal_res[i]
                    if i == "doc_order":
                        doc_order = primal_res[i]
                    if i == "inserted_documents":
                        inserted_documents = primal_res[i]
                    if i == "index":
                        index = primal_res[i]


            for zon in range(index,len(zone)-1):
                index=zon
                z = counter


                while z != -1:
                    url = "https://pflegefinder.bkk-dachverband.de/pflegeberatung/pflegestuetzpunkte/suche.php?searchcontrol%5Bsubmit%5D=1&searchdata%5Bplzort%5D=&searchdata%5Blocation%5D=&searchdata%5Bmaxdistance%5D=20&searchdata%5Bbundesland%5D=" + zone[zon] + "&p=" + str(
                        z)  # looping in every sing page of every filtered bundesland
                    z += 1
                    zx=z
                    driver.get(url)
                    time.sleep(1)
                    cookies_button = driver.find_element_by_id("mkc-btn-select")  # locates the cookie accept button
                    if cookies_button.is_displayed():
                        driver.execute_script("arguments[0].click();", cookies_button)  # clicks the located button
                        time.sleep(2)

                    more_button = driver.find_elements_by_link_text('›')  # locates the "next_page" button
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    res = {}
                    table = soup.find("table", {"class": "table table-striped"}).find("tbody")  # locates the useful table body
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

                    tr = table.findAll("tr")  # gets all the table rows
                    tr_ex = tr[-(20 - doc_order):]
                    for r in tr_ex:

                        fake_name = r.find('a')  # variable representing the name regardless if it exists or not
                        if fake_name == None:
                            continue
                        else:
                            name = fake_name.get_text()
                        print(name)
                        fake_address = r.find("i", {
                            "class": "fas fa-map-marker"})  # variable representing the adress regardless if it exists or not
                        if fake_address != None:
                            address = fake_address.next_sibling.strip()
                            if address == "Ort jährlich wechselnd":  # if the address is constantly changing that means the street and the house number as well
                                street = "Ort jährlich wechselnd"
                                house_number = "Ort jährlich wechselnd"
                            else:
                                street = r.find("strong").next_sibling.strip().replace("- ", "").split(",")[
                                    0].strip()  # extracting the street and removing "-" and "," if they exists
                                house_number = r.find("strong").next_sibling.strip().replace("- ", "").split(",")[
                                    1].strip()  # extracting the house number and removing "-" and "," if they exists
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

                        link = r.find("a", {"style": "color:inherit"}, href=True)  # extracting the nursing base url
                        true_link = "https://pflegefinder.bkk-dachverband.de/pflegeberatung/pflegestuetzpunkte/" + link['href']
                        print(true_link)
                        driver.get(true_link)

                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        content = soup.findAll("div", {"id": "col-landscape"})
                        for c in content:
                            res = nursing_bases_functions.deep_info_extraction(c,
                                                                               res)  # resulted nursing base informations extracted from its specific page

                            final_string = json.dumps(res)
                            print(final_string)
                            file_data = json.loads(final_string)  # converting the result to json
                            print(file_data)
                            final_output = connection_db.insert_new_care_center(
                                file_data)  # inserting the resulted json file to the data base
                            print(final_output)
                            inserted_documents += 1
                            doc_order+=1
                            print(str(inserted_documents) + " documents were inserted so far")
                    counter = zx
                    doc_order = 0

                    error_connection_db.connection_mongo().logs.drop()
                    if len(more_button) == 0 and r == tr_ex[
                        len(tr_ex) - 1]:  # if the next page button is not displayed anymore and if all the data avilble is inserted to th DB
                        break
                counter=1

        except Exception as e:
            print(e)
            res_err = {
                "exit_with_error": 1,
                "offset": counter,
                "doc_order": doc_order,
                "inserted_documents": inserted_documents,
                "index":index

            }

            final_string = json.dumps(res_err)
            print(final_string)
            file_data = json.loads(final_string)  # converting the result to json
            print(file_data)
            final_output = error_connection_db.insert_new_error(
                file_data)  # inserting the resulted json file to the data base
            print(final_output)
            continue

    driver.quit()
    return
