import json
from bs4 import BeautifulSoup
import time
import driver_config
import connection_db
import error_connection_db
import hospitals_functions


def scrape():
    while True:
        driver = driver_config.configure_driver()
        doc_order = 0
        counter = 0
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


            url = "https://klinikfinder.bkk-dachverband.de/suche/suchergebnis.php?searchdata%5Bplzort%5D=Berlin&searchdata%5Blocation%5D=6701%7CAGS&searchdata%5Bmaxdistance%5D=bundesweit&searchcontrol%5Blimit_offset%5D=60&searchcontrol%5Blimit_num%5D=30&searchcontrol%5Border%5D=name"
            driver.get(url)
            time.sleep(1)

            cookies_button = driver.find_element_by_id("mkc-btn-select")  # locates the cookie accept button
            if cookies_button.is_displayed():
                driver.execute_script("arguments[0].click();", cookies_button)  # clicks the located button
                time.sleep(2)

            z = 0
            while z != -1:

                more_button = driver.find_element_by_id("more_btn")  # locates the "show more" button
                for i in range(0, counter):
                    more_button = driver.find_element_by_id("more_btn")  # locates the "show more" button
                    driver.execute_script("arguments[0].click();", more_button)  # clicks the located button
                    time.sleep(1)
                if more_button.is_displayed():
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    res = {}
                    table = soup.find("table")

                    tr = table.findAll("tr")  # gets all the table rows
                    tr_ex=tr[-(30-doc_order):] # gets the last 30 rows of the table
                    for r in tr_ex:
                        link = r.find("a", {"class": "main-link"}, href=True)  # gets the link to each hospital page
                        print(link['href'])
                        driver.get(link['href'])
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')

                        content = soup.findAll("div", {
                            "class": "row rowtable-data"})  # gets all the information about the hospital

                        for c in content:
                            res = hospitals_functions.deep_info_extraction(c,
                                                                           res)  # resulted dictionnary containing all the important information
                        bed_link = link['href'].replace("uebersicht",
                                                        "stationaere-behandlung")  # prepares the true link that leads to the page containing the number of beds and number of annual cases

                        driver.get(bed_link)
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        res = hospitals_functions.bed_info_extraction(soup,
                                                                      res)  # addind the extracted bed information to the previous result
                        final_string = json.dumps(res)
                        print(final_string)
                        file_data = json.loads(final_string)  # converting the result to json
                        print(file_data)
                        final_output = connection_db.insert_new_hospital(
                            file_data)  # inserting the resulted json file to the data base
                        print(final_output)

                        inserted_documents += 1
                        doc_order+=1
                        print(str(inserted_documents) + " documents were inserted so far")
                    counter += 1  # counter that counts how many times the "show more" button should be pressed each time the browser comes back to thee main page

                    doc_order = 0
                    url = "https://klinikfinder.bkk-dachverband.de/suche/suchergebnis.php?searchdata%5Bplzort%5D=Berlin&searchdata%5Blocation%5D=6701%7CAGS&searchdata%5Bmaxdistance%5D=bundesweit&searchcontrol%5Blimit_offset%5D=60&searchcontrol%5Blimit_num%5D=30&searchcontrol%5Border%5D=name"
                    driver.get(url)
                    error_connection_db.connection_mongo().logs.drop()


                    time.sleep(1)
                else:
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    res = {}
                    table = soup.find("table")

                    tr = table.findAll("tr")  # gets all the table rows
                    tr_ex = tr[-(30-doc_order):]  # gets the last 30 rows of the table
                    for r in tr_ex:
                        link = r.find("a", {"class": "main-link"}, href=True)  # gets the link to each hospital page
                        print(link['href'])
                        driver.get(link['href'])
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')

                        content = soup.findAll("div", {
                            "class": "row rowtable-data"})  # gets all the information about the hospital

                        for c in content:
                            res = hospitals_functions.deep_info_extraction(c,
                                                                           res)  # resulted dictionnary containing all the important information
                        bed_link = link['href'].replace("uebersicht",
                                                        "stationaere-behandlung")  # prepares the true link that leads to the page containing the number of beds and number of annual cases

                        driver.get(bed_link)
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        res = hospitals_functions.bed_info_extraction(soup,
                                                                      res)  # addind the extracted bed information to the previous result
                        final_string = json.dumps(res)
                        print(final_string)
                        file_data = json.loads(final_string)  # converting the result to json
                        print(file_data)
                        final_output = connection_db.insert_new_hospital(
                            file_data)  # inserting the resulted json file to the data base
                        print(final_output)

                        inserted_documents += 1
                        doc_order+=1
                        print(str(inserted_documents) + " documents were inserted so far")
                    counter += 1  # counter that counts how many times the "show more" button should be pressed each time the browser comes back to thee main page

                    doc_order = 0
                    url = "https://klinikfinder.bkk-dachverband.de/suche/suchergebnis.php?searchdata%5Bplzort%5D=Berlin&searchdata%5Blocation%5D=6701%7CAGS&searchdata%5Bmaxdistance%5D=bundesweit&searchcontrol%5Blimit_offset%5D=60&searchcontrol%5Blimit_num%5D=30&searchcontrol%5Border%5D=name"
                    driver.get(url)

                    time.sleep(1)
                    error_connection_db.connection_mongo().logs.drop()

                    break

        except Exception as e:
            print(e)
            res_err = {
                "exit_with_error": 1,
                "offset": counter,
                "doc_order": doc_order,
                "inserted_documents": inserted_documents

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
