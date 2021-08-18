def info_extraction(r):
    """extract information from the main page """
    name = r.find("a").get_text()
    print(name)
    address = r.findAll("br")[0].next_sibling.get_text().strip()
    print(address)
    street = address.split(",")[0].strip()
    print(street)
    house_number = address.split(",")[1].strip()
    print(house_number)
    fake_phone = r.find("i", {"class": "fas fa-phone"})
    if fake_phone == None:
        phone = "N/A"
    else:
        phone = fake_phone.next_sibling.strip().replace("Telefon: ", "")

    if phone == "-":
        phone = "N/A"
    print(phone)
    fake_fax = r.find("i", {"class": "fas fa-fax"})
    if fake_fax == None:
        fax = "N/A"
    else:
        fax = fake_fax.next_sibling.strip().replace("Fax: ", "")
    if fax == "-":
        fax = "N/A"
    print(fax)
    fake_mail = r.find("div",
                       {"style": "white-space: nowrap; max-width: 250px; text-overflow: ellipsis; overflow: hidden;"})
    if fake_mail == None:
        mail = "N/A"
    else:
        mail = fake_mail.get_text().strip()
    print(mail)
    res = {'name': name,
           'street': street,
           'house_number': house_number,
           'phone': [phone],
           'fax': fax,
           'mail': mail,
           'branche': 'health',
           'category': 'care',
           'number_of_beds': 'N/A',
           'number_short_time_care': 'N/A',
           'number_single_room': 'N/A',
           'number_double_room': 'N/A',
           'contact_person_fname': 'N/A',
           'contact_person_lname': 'N/A',
           'contact_person_salutation': 'N/A'
           }
    return res


def deep_info_extraction(content, res):
    """extracts more information from each page """
    website = "N/A"
    identification_number = "N/A"
    for c in content:
        fake_website = c.find("a", {"target": "_blank"})

        if fake_website != None:
            website = fake_website.get_text().strip().replace(" ", "")
            if website == "-":
                website = "N/A"

        fake_identification_number = content[1].find("br")
        if fake_identification_number != None:
            identification_number = fake_identification_number.next_sibling.strip()

    print(website)
    print(identification_number)
    res["website"] = website
    res["identification_number"] = identification_number
    return res
