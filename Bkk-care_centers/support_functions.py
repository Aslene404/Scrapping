def info_extraction(r,res):
    """extract information from the main page """
    name = "N/A"
    street = "N/A"
    house_number = "N/A"
    name = r.findAll("strong")[1].get_text()
    print(name)
    fake_address = r.find("i", {"class": "fas fa-map-marker"})
    if fake_address != None:
        address = fake_address.next_sibling.strip()
        if address == "Ort jährlich wechselnd":
            street = "Ort jährlich wechselnd"
            house_number = "Ort jährlich wechselnd"
        else:
            street = r.findAll("strong")[2].next_sibling.strip().replace("- ", "").split(",")[0].strip()
            house_number = r.findAll("strong")[2].next_sibling.strip().replace("- ", "").split(",")[1].strip()
    print(street)
    print(house_number)
    res = {'name': name,
           'street': street,
           'house_number': house_number,
           'branche': 'health',
           'category': 'care'}
    return(res)
def deep_info_extraction(c,res):
    """extracts more information from each page """
    phone = "N/A"
    fax = "N/A"
    mail = "N/A"
    website = "N/A"
    identification_number = "N/A"
    number_of_beds = "N/A"
    number_short_time_care = "N/A"
    number_single_room = "N/A"
    number_double_room = "N/A"
    contact_person_fname = ""
    contact_person_lname = "N/A"
    contact_person_salutation = "N/A"
    info = c.find("div", {"class", "col-sm-12 col-xs-12"})
    fake_phone = info.find("i", {"class", "fas fa-phone"})
    if fake_phone == None:
        phone = "N/A"
    else:
        phone = fake_phone.next_sibling.strip().replace("Telefon: ", "")

    if phone == "-":
        phone = "N/A"
    print(phone)

    fake_fax = info.find("i", {"class", "fas fa-fax"})
    if fake_fax == None:
        fax = "N/A"
    else:
        fax = fake_fax.next_sibling.strip().replace("Telefax: ", "")

    if fax == "-":
        fax = "N/A"
    print(fax)

    fake_mail = info.find("a")

    if fake_mail != None:
        mail = fake_mail.get_text().strip().replace(" ", "")
    if mail == "-":
        mail = "N/A"
    print(mail)
    fake_website = info.find("i", {"class", "fas fa-globe"})
    if fake_website != None:
        website = fake_website.next_sibling.next_sibling.get_text()
    print(website)

    res["phone"] = [phone]
    res["fax"] = fax
    res["mail"] = mail
    res["website"] = website
    res["number_of_beds"]=number_of_beds

    res["identification_number"] = identification_number
    res["number_short_time_care"] = number_short_time_care
    res["number_single_room"] = number_single_room
    res["number_double_room"] = number_double_room
    res["contact_person_fname"] = contact_person_fname
    res["contact_person_lname"] = contact_person_lname
    res["contact_person_salutation"] = contact_person_salutation
    return res
