def info_extraction(r, res):
    """extract information from the main page """
    name = r.find("a").get_text()
    print(name)
    street = r.findAll("td")[1].findAll("div")[0].get_text()
    print(street)
    house_number = r.findAll("td")[1].findAll("div")[1].get_text()
    print(house_number)
    number_of_beds = r.findAll("td")[2].get_text()
    if number_of_beds == "k.A.":
        number_of_beds = "N/A"
    print(number_of_beds)
    res = {'name': name,
           'street': street,
           'house_number': house_number,
           'branche': 'health',
           'category': 'care',
           'number_of_beds': number_of_beds,

           }
    return res


def deep_info_extraction(content, res):
    """extracts more information from each page """
    phone = "N/A"

    fax = "N/A"
    mail = "N/A"
    website = "N/A"
    identification_number = "N/A"
    number_short_time_care = "N/A"
    number_single_room = "N/A"
    number_double_room = "N/A"
    contact_person_fname = ""
    contact_person_lname = "N/A"
    contact_person_salutation = "N/A"
    fake_phone = content[0].find("i", {"class": "fas fa-phone"})
    if fake_phone == None:
        phone = "N/A"
    else:
        phone = fake_phone.next_sibling.strip().replace("Telefon: ", "")

    if phone == "-":
        phone = "N/A"
    print(phone)

    fake_fax = content[0].find("i", {"class": "fas fa-fax"})
    if fake_fax == None:
        fax = "N/A"
    else:
        fax = fake_fax.next_sibling.strip().replace("Fax: ", "")

    if fax == "-":
        fax = "N/A"
    print(fax)

    fake_mail = content[0].find("a")

    if fake_mail != None:
        mail = fake_mail.get_text().strip().replace(" ", "")
    if mail == "-":
        mail = "N/A"
    print(mail)

    fake_website = content[0].find("a", {"target": "_blank"}, href=True)

    if fake_website != None:
        website = fake_website['href']
    if website == "-":
        website = "N/A"
    print(website)
    fake_identification_number = content[1].findAll("br")
    if fake_identification_number != None:
        identification_number = fake_identification_number[len(fake_identification_number) - 1].next_sibling.strip()

        for fi in fake_identification_number:
            if fi.next_sibling.strip().find("davon Anzahl der Plätze für Kurzzeitpflege: ") != -1:
                number_short_time_care = fi.next_sibling.strip().replace("davon Anzahl der Plätze für Kurzzeitpflege: ",
                                                                         "")

            if fi.next_sibling.strip().find("Anzahl der Plätze in Einzelzimmer: ") != -1:
                number_single_room = fi.next_sibling.strip().replace("Anzahl der Plätze in Einzelzimmer: ", "")

            if fi.next_sibling.strip().find("Anzahl der Plätze in Doppelzimmer: ") != -1:
                number_double_room = fi.next_sibling.strip().replace("Anzahl der Plätze in Doppelzimmer: ", "")

    print(identification_number)
    print(number_short_time_care)
    print(number_single_room)
    print(number_double_room)
    contact_person = content[0].findAll("strong")

    if contact_person != None:
        for cp in contact_person:
            if cp.get_text().find("Kontaktperson der Einrichtung:") != -1:
                contact_person_x = cp.next_sibling.next_sibling.strip()
                print(contact_person_x)

                if contact_person_x.find("-") != -1:
                    print(cp.next_sibling.next_sibling.strip().split("-"))
                    print(cp.next_sibling.next_sibling.strip().split("-")[0].strip())
                    contact_person_x = cp.next_sibling.next_sibling.strip().split("-")[0].strip()

                if contact_person_x.find(",") != -1:
                    contact_person_x = cp.next_sibling.next_sibling.strip().split(",")[0].strip()
                print(contact_person_x)

                cpx = contact_person_x.split(" ")
                if cpx[0] == "Frau" or cpx[0] == "Herr":
                    contact_person_salutation = cpx[0]
                    cpx.pop(0)
                contact_person_lname = cpx[len(cpx) - 1].strip()
                if contact_person_lname[0] == "(":
                    cpx.pop(len(cpx) - 1)
                    contact_person_lname = cpx[len(cpx) - 1]
                cpx.pop(len(cpx) - 1)
                for xpc in cpx:
                    contact_person_fname += xpc

    if contact_person_fname == "":
        contact_person_fname = "N/A"
    print(contact_person_salutation)
    print(contact_person_fname)
    print(contact_person_lname)
    res["phone"] = [phone]
    res["fax"] = fax
    res["mail"] = mail
    res["website"] = website

    res["identification_number"] = identification_number
    res["number_short_time_care"] = number_short_time_care
    res["number_single_room"] = number_single_room
    res["number_double_room"] = number_double_room
    res["contact_person_fname"] = contact_person_fname
    res["contact_person_lname"] = contact_person_lname
    res["contact_person_salutation"] = contact_person_salutation
    return res
