import json
import random
from bs4 import BeautifulSoup
import time
import driver_config
import connection_db
import error_connection_db


def scrape():
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
        company_list=list(companies.find({}, {"_id": 0, "name": 1,
                                     "registered_address": 1}))
        for x in range(counter,len(company_list)-1):  # loop through the companies having a name and address
            print(company_list[x])
            counter+=1

            if len(company_list[x]) == 2:  # if both elements are found
                postcode = company_list[x]["registered_address"].strip()
                postcode = postcode.split(" ")
                for i in range(len(postcode) - 1, 0, -1):  # loop backwards in the obtained string
                    if postcode[i].strip().isdigit():  # if the obtained string fully a number
                        postcode = postcode[i].strip()
                        break

                keyword = company_list[x]["name"].strip().replace(" ",
                                                    "%20").strip()  # gets the name and replaces empty spaces with "%20" in order to be used as a keyword in the url
                keyword = keyword.replace("&",
                                          "%26").strip()  # gets the name and replaces & symbols with "%26" in order to be used as a keyword in the url
                print(postcode)
                print(keyword)

                url = "https://www.xing.com/search/companies?zip_code=" + postcode + "&keywords=" + keyword  # making the full url of the search operation
                driver.get(url)
                time.sleep(1)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                res = {}

                table = soup.find("div", {"role": "list"})  # gets the useful div element

                tr = table.findAll("div", {"class": "search-card-style-container-69860b53"})  # gets all table rows
                if len(tr) == 1:  # only access if we obtain one result from the search operation
                    for r in tr:
                        name = r.find("div", {"class": "search-card-style-content-20754fd7"}).findAll("div")[
                            0].get_text().strip()  # gets the company name
                        print(name)
                        address = r.find("div", {"class": "search-card-style-content-20754fd7"}).findAll("div")[
                            1].get_text().strip()  # gets the company address
                        print(address)
                        ort = address.split(",")[0].strip()  # splitting the address with "," and using the first part as ort
                        print(ort)
                        bundesland = address.split(",")[
                            1].strip()  # splitting the address with "," and using the second part as bundeslan
                        print(bundesland)
                        fake_numbers = r.findAll("span", {
                            "class": "CompanyCard-style-minorCopy-b61c6828"})  # variable representing the xing users number and workers number regardless if they exists or not
                        if len(fake_numbers) == 0:  # if both numbers are not available
                            xing_users = "N/A"
                            worker_range = "N/A"
                        if len(fake_numbers) == 1 and fake_numbers[
                            0].get_text().strip() == "XING members:":  # if only the xing users number is available
                            xing_users = fake_numbers[0].next_sibling.strip()
                            worker_range = "N/A"
                        if len(fake_numbers) == 1 and fake_numbers[
                            0].get_text().strip() == "Employees:":  # if only the worker range number is available
                            worker_range = fake_numbers[0].next_sibling.strip().replace(" employees",
                                                                                        "").strip()  # gets the worker range number and replace " employees" at the end of the obtained string
                            xing_users = "N/A"
                        if len(fake_numbers) >= 2:
                            xing_users = fake_numbers[0].next_sibling.strip()
                            worker_range = fake_numbers[1].next_sibling.strip().replace(" employees",
                                                                                        "").strip()  # gets the worker range number and replace " employees" at the end of the obtained string

                        print(xing_users)
                        print(worker_range)
                        res = {
                            'name': name,
                            'ort': ort,
                            'bundesland': bundesland,
                            'xing_users': xing_users,
                            'worker_range': worker_range

                        }
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
