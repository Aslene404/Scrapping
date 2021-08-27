import json

from bs4 import BeautifulSoup
import time
import driver_config
import connection_db
import error_connection_db
import xing_functions


def scrape():
    while True:
        driver = driver_config.configure_driver()
        doc_order = 0
        counter = 0
        inserted_documents = 0  # counter to count the number of inserted documents to the database
        companies = connection_db.connection_mongo_to_companies()  # get all the companies from existing DB
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

            url = "https://login.xing.com/?dest_url=https%3A%2F%2Fwww.xing.com%2Fsearch%2Fcompanies"
            driver.get(url)
            time.sleep(3)
            cookies_button = driver.find_element_by_id("consent-accept-button")  # locates the cookie accept button
            if cookies_button.is_displayed():
                driver.execute_script("arguments[0].click();", cookies_button)  # clicks the located button
                time.sleep(2)
            username = "aslenerazor@gmail.com"  # personal account's username
            password = "shadow11820977"  # personal account's password
            driver.find_element_by_id("username").send_keys(
                username)  # locate the input field for the username and fill it with given username
            driver.find_element_by_id("password").send_keys(
                password)  # locate the input field for the password and fill it with given password
            driver.find_element_by_css_selector(".fYOVsO").click()  # locate the login button and click it
            time.sleep(3)
            company_list = list(companies.find({}, {"_id": 0, "name": 1,
                                                    "registered_address": 1}))  # gets companies with a name and address
            for x in range(counter, len(company_list) - 1):  # loop through the companies having a name and address

                counter += 1

                if len(company_list[x]) == 2:  # if both the name and registered_address are found

                    url = xing_functions.url_construction(
                        company_list[x])  # returns the url containing the keyword and the postcode of the company
                    driver.get(url)
                    time.sleep(1)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    table = soup.find("div", {"role": "list"})  # gets the useful div element

                    tr = table.findAll("div", {"class": "search-card-style-container-69860b53"})  # gets all table rows
                    if len(tr) == 1:  # only access if we obtain one result from the search operation
                        for r in tr:
                            res = xing_functions.info_extraction(r)
                            final_string = json.dumps(res)
                            print(final_string)
                            file_data = json.loads(final_string)  # converting the result to json
                            print(file_data)
                            final_output = connection_db.insert_new_company(
                                file_data)  # inserting the resulted json file to the data base
                            print(final_output)
                            inserted_documents += 1
                            print(str(inserted_documents) + " documents were inserted so far")
            error_connection_db.connection_mongo().logs.drop()

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
