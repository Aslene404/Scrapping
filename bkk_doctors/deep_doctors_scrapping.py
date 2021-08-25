import json
from bs4 import BeautifulSoup

import time
import driver_config
import connection_db
import doctors_functions
import error_connection_db


def scrape():
    driver = driver_config.configure_driver()
    url_res=list(connection_db.get_doctor_url())
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
        for ur in range(inserted_documents,len(url_res)-1):
            url=url_res[ur]['source_url']


            driver.get(url)
            time.sleep(1)
            cookies_button = driver.find_element_by_id("mkc-btn-select")  # locates the cookie accept button
            if cookies_button.is_displayed():
                driver.execute_script("arguments[0].click();", cookies_button)  # clicks the located button
                time.sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.findAll("div", {"id": "maincontent"})  # gets all the information about the doctor
            res=connection_db.get_doctor_info(url)
            print(res)
            for c in content:
                res_ex = doctors_functions.deep_info_extraction(c, res)

                filter = {'source_url': url}


                newvalues = {"$set": res_ex}


                output=connection_db.connection_mongo().doctors.update_one(filter, newvalues)
                print(output)
                inserted_documents += 1
                print(str(inserted_documents) + " documents were updated so far")
    except:
        res_err = {
            "exit_with_error": 1,
            "offset": counter,
            "doc_order": inserted_documents,
            "inserted_documents": inserted_documents

        }

        final_string = json.dumps(res_err)
        print(final_string)
        file_data = json.loads(final_string)  # converting the result to json
        print(file_data)
        final_output = error_connection_db.insert_new_error(
            file_data)  # inserting the resulted json file to the data base
        print(final_output)

        driver.quit()
    return



