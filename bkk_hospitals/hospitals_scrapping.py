import json
from bs4 import BeautifulSoup
import time
import driver_config
import connection_db
import hospitals_functions
def scrape():
    driver = driver_config.configure_driver()

    url = "https://klinikfinder.bkk-dachverband.de/suche/suchergebnis.php?searchdata%5Bplzort%5D=Berlin&searchdata%5Blocation%5D=6701%7CAGS&searchdata%5Bmaxdistance%5D=bundesweit&searchcontrol%5Blimit_offset%5D=60&searchcontrol%5Blimit_num%5D=30&searchcontrol%5Border%5D=name"
    driver.get(url)
    time.sleep(1)

    cookies_button = driver.find_element_by_id("mkc-btn-select")
    if cookies_button.is_displayed():
        driver.execute_script("arguments[0].click();", cookies_button)
        time.sleep(2)
    z = 0
    while z != -1:

        more_button = driver.find_element_by_id("more_btn")
        if more_button.is_displayed():
            driver.execute_script("arguments[0].click();", more_button)

            time.sleep(1)
        else:
            break
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    res = {}
    table = soup.find("table")

    tr = table.findAll("tr")
    for r in tr:
        link = r.find("a", {"class": "main-link"}, href=True)
        print(link['href'])
        driver.get(link['href'])
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        content = soup.findAll("div", {"class": "row rowtable-data"})

        for c in content:
            res=hospitals_functions.deep_info_extraction(c,res)
        bed_link = link['href'].replace("uebersicht", "stationaere-behandlung")

        driver.get(bed_link)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        res=hospitals_functions.bed_info_extraction(soup,res)
        final_string = json.dumps(res)
        print(final_string)
        file_data = json.loads(final_string)
        print(file_data)
        final_output = connection_db.insert_new_hospital(file_data)
        print(final_output)
    driver.quit()
    return
