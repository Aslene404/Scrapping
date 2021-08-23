from bs4 import BeautifulSoup
import connection_db
from bkk_hospitals import connection_db as connection_db_hospital


def deep_info_extraction(c):
    """extracts more information from each page """
    collegues = []
    name = c.find("h1").get_text()
    print(name)
    salutation = name.split()[0]  # the first word of the whole extracted name (usally Frau or Herr)
    print(salutation)
    proto = name.split(' ', 1)[1]  # gets the rest of the name after the salutation
    print(proto)
    splits = proto.split()
    title = ""
    for split in splits:
        if len(split) == 2 or split.find("-") != -1 and split.find("-") != 0:
            break
        if split[len(split) - 1] == "." or split[len(split) - 1] == ")":
            title += split + " "  # add all the found titles into one string

    print(title)
    first_last = proto.replace(title, "")  # remove title from the rest of the name after the salutation
    print(first_last)
    first_name = first_last.split()[0]  # gets the first name from the full name
    print(first_name)
    last_name = first_last.split(' ', 1)[1]  # gets the last name from the full name
    print(last_name)
    info = c.findAll("div", {"class": "col-sm-6 col-xs-12"})  # gets all contact information from the page

    street = info[0].findAll("br")[0].next_sibling.strip()  # gets the street from the contact informations
    print(street)
    house_number = info[0].findAll("br")[1].next_sibling.strip()  # gets the house number from the contact informations
    print(house_number)
    phone = info[0].find("i", {"class": "fa fa-phone"}).next_sibling.strip().replace("Telefon: ",
                                                                                     "")  # gets the phone number from the contact informations and removes the Telefon: from the obtained string

    if phone == "":
        phone = "N/A"
    print(phone)
    fax = info[0].find("i", {"class": "fa fa-fax"}).next_sibling.strip().replace("Fax: ",
                                                                                 "")  # gets the fax number from the contact informations and removes the Fax: from the obtained string

    if fax == "":
        fax = "N/A"
    print(fax)
    true_website = "N/A"

    website = info[0].findAll("a")  # gets all the links from the contact informations
    for web in website:
        true_website = web.get_text()
        print(true_website)
    health_insurance_approval = info[1].findAll("br")[0].next_sibling.strip()
    print(health_insurance_approval)
    if health_insurance_approval == "Ja":
        health_insurance_approval = True
        print(health_insurance_approval)
    if health_insurance_approval == "Nein":
        health_insurance_approval = False
        print(health_insurance_approval)
    if health_insurance_approval == "Nicht bekannt":
        health_insurance_approval = "N/A"
        print(health_insurance_approval)

    family_doctor = info[1].findAll("br")[1].next_sibling.strip()
    print(family_doctor)
    if family_doctor == "Ja":
        family_doctor = True
        print(family_doctor)
    if family_doctor == "Nein":
        family_doctor = False
        print(family_doctor)
    if family_doctor == "Nicht bekannt":
        family_doctor = "N/A"
        print(family_doctor)

    home_visits = info[1].findAll("br")[2].next_sibling.strip()
    print(home_visits)
    if home_visits == "Ja":
        home_visits = True
        print(home_visits)
    if home_visits == "Nein":
        home_visits = False
        print(home_visits)
    if home_visits == "Nicht bekannt":
        home_visits = "N/A"
        print(home_visits)
    group_practice = info[1].findAll("br")[3].next_sibling.strip()
    print(group_practice)
    if group_practice == "Ja":
        group_practice = True
        print(group_practice)

        colle = info[1].findAll("a")
        for co in colle:
            print(co.get_text().strip())
            collegues.append(co.get_text().strip())
        print(collegues)
    if group_practice == "Nein":
        group_practice = False
        print(group_practice)
    if group_practice == "Nicht bekannt":
        group_practice = "N/A"
        print(group_practice)
    spec = c.findAll("div", {"class": "row rowtable-data"})
    specialties = []
    for sp in spec:
        lis = sp.findAll("li")

        for li in lis:
            print(li.get_text().strip())
            specialties.append(li.get_text().strip())
    print(specialties)
    myclinic = ""
    cli = connection_db_hospital.get_clinic_by_street_nb_house(street,
                                                               house_number)  # gets the matching clinic for the doctor's address

    print(cli)
    if cli != None:
        for i in cli:
            if i == "name":
                myclinic = cli[i]  # gets the clinic's name
                print(myclinic)

    res = {
        'verification_name': name,
        'title': title,
        'salutation': salutation,
        'first_name': first_name,
        'last_name': last_name,
        'street': street,
        'house_number': house_number,
        'branche': 'health',
        'category': 'doctors',
        'phone': [phone],
        'website': true_website,
        'fax': fax,
        'specialty': specialties,
        'clinic': myclinic,
        'health_insurance_approval': health_insurance_approval,
        'family_doctor': family_doctor,
        'home_visits': home_visits,
        'group_practice': group_practice,
        'collegues': collegues,
        'exit_with_error': 0}
    return res


def get_doctor_urls(driver):
    """returns the latest 20 url from the main page"""
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("tbody")
    urls = []

    tr = table.findAll("tr")
    y = 1
    tr_ex = tr[-20:]

    for r in tr_ex:
        link = r.find("a", href=True)
        true_link = "https://arztfinder.bkk-dachverband.de/suche/" + link['href']
        print(str(y) + true_link)
        y += 1
        urls.append(true_link)
    return urls


def info_extraction(r):
    """extracts information from the first page"""
    true_link = "https://arztfinder.bkk-dachverband.de/suche/" + r.find("a", href=True)['href']
    print(true_link)
    name = r.find("a", href=True).get_text().strip()
    print(name)

    salutation = name.split()[0]
    print(salutation)
    proto = name.split(' ', 1)[1]
    print(proto)
    splits = proto.split()
    title = ""
    for split in splits:
        if len(split) == 2 or split.find("-") != -1 and split.find("-") != 0:
            break
        if split[len(split) - 1] == "." or split[len(split) - 1] == ")":
            title += split + " "

    print(title)
    first_last = proto.replace(title, "")
    print(first_last)
    first_name = first_last.split()[0]
    print(first_name)
    last_name = first_last.split(' ', 1)[1]
    print(last_name)
    specialities = []
    spec = r.find("span", {"class": "fachrichtung"}).get_text().strip().replace("(", "").strip().replace(")",
                                                                                                         "").strip().replace(
        "Facharzt für ", "").strip().replace("FA f. ", "").strip()
    spec = spec.split(",")
    for sp in spec:
        specialities.append(sp.strip())
    print(specialities)

    street = r.findAll("br")[1].next_sibling.strip()
    print(street)
    house_number = r.findAll("br")[2].next_sibling.strip()
    print(house_number)
    myclinic = ""
    cli = connection_db_hospital.get_clinic_by_street_nb_house(street, house_number)

    print(cli)
    if cli != None:
        for i in cli:
            if i == "name":
                myclinic = cli[i]
                print(myclinic)

    res2 = {
        'verification_name': name,
        'title': title,
        'salutation': salutation,
        'first_name': first_name,
        'last_name': last_name,
        'street': street,
        'house_number': house_number,
        'branche': 'health',
        'category': 'doctors',
        'clinic': myclinic,
        'source_url': true_link,
        'exit_with_error': 0
    }

    return res2
