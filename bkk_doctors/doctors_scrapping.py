import json
from bs4 import BeautifulSoup

import time
import driver_config
import connection_db
import doctors_functions


def scrape():
    driver = driver_config.configure_driver()
    url = "https://arztfinder.bkk-dachverband.de/suche/suchergebnis.php"
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
    urls = doctors_functions.get_doctor_urls(driver)
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
    driver.quit()
    return
