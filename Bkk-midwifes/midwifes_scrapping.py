import json

from bs4 import BeautifulSoup
import time
import driver_config
import connection_db
import error_connection_db
import midwifes_functions


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
            url = "https://hebammenfinder.bkk-dachverband.de/suche/suchergebnis.php"
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
                    res = {}  # initiate resulted dictionary
                    table = soup.find("table")

                    tr = table.findAll("tr")  # gets all the table rows
                    tr_ex=tr[-(20-doc_order):] # gets the last 20 rows of the table
                    th = table.findAll("th")  # gets all the table headers
                    schwangerenvorsorge = False
                    hausgeburt = False
                    beleggeburt = False
                    geburtshausgeburt = False
                    wochenbettbetreuung = False
                    kurse = False


                    for r in tr_ex:

                        td = r.findAll("td")
                        data = []
                        for d in td:
                            res = midwifes_functions.info_extraction(d, res)  # resulted informations
                            data = midwifes_functions.service_extraction(d, data)  # array containing the midwife's service

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
                        file_data = json.loads(final_string)  # converting the result to json
                        if data != []:
                            final_output = connection_db.insert_new_midwife(
                                file_data)  # inserting the resulted json file to the data base
                            print(final_output)
                            inserted_documents += 1
                            doc_order+=1
                            print(str(inserted_documents) + " documents were inserted so far")
                    counter += 1  # counter that counts how many times the "show more" button should be pressed each time the browser comes back to thee main page

                    doc_order = 0
                    url = "https://hebammenfinder.bkk-dachverband.de/suche/suchergebnis.php"
                    driver.get(url)
                    error_connection_db.connection_mongo().logs.drop()

                    time.sleep(1)
                else:
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    res = {}  # initiate resulted dictionary
                    table = soup.find("table")

                    tr = table.findAll("tr")  # gets all the table rows
                    tr_ex = tr[-(20-doc_order):]
                    th = table.findAll("th")  # gets all the table headers
                    schwangerenvorsorge = False
                    hausgeburt = False
                    beleggeburt = False
                    geburtshausgeburt = False
                    wochenbettbetreuung = False
                    kurse = False


                    for r in tr_ex:

                        td = r.findAll("td")
                        data = []
                        for d in td:
                            res = midwifes_functions.info_extraction(d, res)  # resulted informations
                            data = midwifes_functions.service_extraction(d, data)  # array containing the midwife's service

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
                        file_data = json.loads(final_string)  # converting the result to json
                        if data != []:
                            final_output = connection_db.insert_new_midwife(
                                file_data)  # inserting the resulted json file to the data base
                            print(final_output)
                            inserted_documents += 1
                            doc_order+=1
                            print(str(inserted_documents) + " documents were inserted so far")
                    counter += 1  # counter that counts how many times the "show more" button should be pressed each time the browser comes back to thee main page

                    doc_order = 0
                    url = "https://hebammenfinder.bkk-dachverband.de/suche/suchergebnis.php"
                    driver.get(url)
                    error_connection_db.connection_mongo().logs.drop()

                    time.sleep(1)
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
        break
    return
