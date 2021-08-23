import json

from bs4 import BeautifulSoup
import time
import driver_config
import connection_db
import nursing_homes_functions


def scrape():
    driver = driver_config.configure_driver()
    inserted_documents = 0  # counter to count the number of inserted documents to the database

    z = 0
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

        for r in tr:
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
            print(str(inserted_documents) + " documents were inserted so far")

    driver.quit()
    return
