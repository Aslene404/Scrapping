import json

from bs4 import BeautifulSoup
import time
import driver_config
import connection_db
import error_connection_db
import nursing_homes_functions


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
            z = counter
            while z != -1:

                url = "https://pflegefinder.bkk-dachverband.de/pflegeheime/searchresult.php?searchdata%5BmaxDistance%5D=0#/limit/20/offset/" + str(
                    z)
                z += 20
                zx = z  # variable representing the latest treated page

                driver.get(url)
                time.sleep(3)

                cookies_button = driver.find_element_by_id("mkc-btn-select")  # locates the cookie accept button
                if cookies_button.is_displayed():
                    driver.execute_script("arguments[0].click();", cookies_button)  # clicks the located button
                    time.sleep(2)

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                res = {}
                next_button = soup.findAll(
                    "a")  # locates all the links in the page including the "next page" button if it exists
                for nb in next_button:
                    print(nb.get_text().strip())
                    if nb.get_text().strip() != "›":  # if the "next page" button is not displayed the system quits after completeing the all the available data
                        z = -1
                    if nb.get_text().strip() == "›":
                        z = zx
                        break

                table = soup.find("table", {"id": "table-pei"}).find("tbody")  # locates the useful table body

                tr = table.findAll("tr")  # locates the table rows
                tr_ex = tr[-(20-doc_order):]

                for r in tr_ex:
                    res = nursing_homes_functions.info_extraction(r,
                                                                  res)  # resulted dictionary containing the informations from the main page

                    link = r.find("a", href=True)  # gets the url of each nursing home
                    print(link['href'])
                    driver.get(link['href'])

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    content = soup.findAll("div", {"class": "col-sm-6 col-xs12"})  # gets the contact information section

                    if len(content) != 0:  # if the page is accessible
                        res = nursing_homes_functions.deep_info_extraction(content,
                                                                           res)  # resulted dictionary containing the informations from the specific nursing homes's page

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
                counter=z
                doc_order=0
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
