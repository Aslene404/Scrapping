import json
from bs4 import BeautifulSoup

import time
import driver_config
import connection_db
import doctors_functions


def scrape():
    driver = driver_config.configure_driver()
    res = {}  # initiate resulted dictionary
    doc_order = 0
    counter = 0
    inserted_documents = 0  # counter to count the number of inserted documents to the database

    try:

        primal_res = connection_db.is_exit_with_error()  # get the latest document inserted before the error
        print(primal_res)
        if primal_res != None:
            for i in primal_res:
                if i == "offset":
                    counter = primal_res[i]
                if i == "doc_order":
                    doc_order = primal_res[i]
                if i == "inserted_documents":
                    inserted_documents = primal_res[i]

        url = "https://arztfinder.bkk-dachverband.de/suche/suchergebnis.php"
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
                table = soup.find("tbody")
                tr = table.findAll("tr")  # gets all the table rows
                tr_ex = tr[-(20 - doc_order):]  # gets the last 20 rows of the table

                """urls = doctors_functions.get_doctor_urls(driver)#returnsa list containing the url of each doctor's page
                counter+=1
                for slru in urls:
                    driver.get(slru)
                    time.sleep(1)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    content = soup.findAll("div", {"id": "maincontent"})#gets all the information about the doctor
                    for c in content:
                        res = doctors_functions.deep_info_extraction(c)#resulted dictionnary containing all the important information
                        res["source_url"]=slru#adding the each url of doctor to the resulted dictionnary 
                        final_string = json.dumps(res)
                        print(final_string)
                        file_data = json.loads(final_string)#converting the result to json
                        print(file_data)
                        final_output = connection_db.insert_new_doctor(file_data)#inserting the resulted json file to the data base
                        print(final_output)
                        inserted_documents+=1
                        print(str(inserted_documents)+" documents were inserted so far")"""
                counter += 1  # counter that counts how many times the "show more" button should be pressed each time the browser comes back to thee main page
                for r in tr_ex:
                    res = doctors_functions.info_extraction(
                        r)  # resulted dictionnary containing the external information about the doctor showed in the main page only

                    final_string = json.dumps(res)
                    print(final_string)
                    file_data = json.loads(final_string)  # converting the result to json
                    print(file_data)
                    final_output = connection_db.insert_new_doctor(
                        file_data)  # inserting the resulted json file to the data base
                    print(final_output)
                    inserted_documents += 1
                    print(str(inserted_documents) + " documents were inserted so far")
                doc_order = 0
                url = "https://arztfinder.bkk-dachverband.de/suche/suchergebnis.php"
                driver.get(url)
                time.sleep(1)

            else:

                """urls = doctors_functions.get_doctor_urls(driver)
                counter += 1
                for slru in urls:
                    driver.get(slru)
                    time.sleep(1)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    content = soup.findAll("div", {"id": "maincontent"})
                    for c in content:
                        res = doctors_functions.deep_info_extraction(c)
                        final_string = json.dumps(res)
                        print(final_string)
                        file_data = json.loads(final_string)
                        print(file_data)
                        final_output = connection_db.insert_new_doctor(file_data)
                        print(final_output)
                        inserted_documents += 1
                        print(str(inserted_documents) + " documents were inserted so far")"""

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                table = soup.find("tbody")
                tr = table.findAll("tr")
                tr_ex = tr[-(20 - doc_order):]
                for r in tr_ex:
                    res = doctors_functions.info_extraction(r)
                    final_string = json.dumps(res)
                    print(final_string)
                    file_data = json.loads(final_string)
                    print(file_data)
                    final_output = connection_db.insert_new_doctor(file_data)
                    print(final_output)
                    inserted_documents += 1
                    print(str(inserted_documents) + " documents were inserted so far")
                doc_order = 0
                url = "https://arztfinder.bkk-dachverband.de/suche/suchergebnis.php"
                driver.get(url)
                time.sleep(1)
                break
    except:
        res["exit_with_error"] = 1
        res["offset"] = counter
        res["doc_order"] = inserted_documents - (20 * (counter))
        res["inserted_documents"] = inserted_documents
        final_string = json.dumps(res)
        print(final_string)
        file_data = json.loads(final_string)  # converting the result to json
        print(file_data)
        final_output = connection_db.insert_new_doctor(file_data)  # inserting the resulted json file to the data base
        print(final_output)

    driver.quit()
    return
