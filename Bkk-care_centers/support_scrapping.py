import json

from bs4 import BeautifulSoup
import time
import driver_config
import connection_db
import support_functions


def scrape():
    driver = driver_config.configure_driver()
    url = "https://pflegefinder.bkk-dachverband.de/aua/searchresult.php?searchdata%5Brequired%5D=1&searchdata%5Boffer_name%5D=&searchdata%5Bzip%5D=&searchdata%5Blocation%5D=&searchdata%5Bmaxdistance%5D=5&searchdata%5Btarget_group%5D=&searchdata%5Bage_group%5D=&searchdata%5Blanguage%5D=&searchdata%5Bsort%5D=distance_asc&searchdata%5Brecord_offset%5D=0"
    driver.get(url)
    time.sleep(1)
    cookies_button = driver.find_element_by_id("mkc-btn-select")  # locates the cookie accept button
    if cookies_button.is_displayed():
        driver.execute_script("arguments[0].click();", cookies_button)  # clicks the located button
        time.sleep(2)
    inserted_documents = 1  # counter to count the number of inserted documents to the database
    z = 0
    while z != -1:

        more_button = driver.find_element_by_id("more_btn")  # locates the "show more" button

        if more_button.is_displayed():
            driver.execute_script("arguments[0].click();", more_button)  # clicks the located button
            time.sleep(1)

        else:
            break
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    res = {}
    table = soup.find("tbody", {"id": "search_result_table_body"})  # gets the useful table body

    tr = table.findAll("tr")  # gets all table rows
    for r in tr:
        res = support_functions.info_extraction(r,
                                                res)  # resulted dictionary containing the informations from the main page

        link = r.find("a", {"style": "color:inherit"}, href=True)  # gets the urls for the center's specific page
        true_link = "https://pflegefinder.bkk-dachverband.de/aua/" + link['href']
        print(true_link)
        driver.get(true_link)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.findAll("div", {"id": "maincontent"})  # locates the contact informations section
        for c in content:
            res = support_functions.deep_info_extraction(c,
                                                         res)  # resulted dictionary containing the information about the center from its specific page

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
