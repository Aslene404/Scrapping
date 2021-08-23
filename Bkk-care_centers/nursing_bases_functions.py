def deep_info_extraction(c, res):
    """extracts more information from each page"""
    phone = "N/A"
    fax = "N/A"
    mail = "N/A"
    website = "N/A"
    fake_phone = c.find("i", {"class",
                              "fas fa-phone"})  # variable representing the phone number regardless if it exists or not
    if fake_phone == None:
        phone = "N/A"
    else:
        phone = fake_phone.next_sibling.strip().replace("Telefon: ",
                                                        "")  # gets the phone number from the contact informations and removes the Telefon: from the obtained string

    if phone == "k.A.":
        phone = "N/A"
    print(phone)
    fake_fax = c.find("i",
                      {"class", "fas fa-fax"})  # variable representing the fax number regardless if it exists or not

    if fake_fax == None:
        fax = "N/A"
    else:
        fax = fake_fax.next_sibling.strip().replace("Fax: ",
                                                    "")  # gets the fax number from the contact informations and removes the Fax: from the obtained string

    if fax == "-":
        fax = "N/A"
    print(fax)

    fake_mail = c.find("i",
                       {"class", "fas fa-envelope"})  # variable representing the email regardless if it exists or not

    if fake_mail != None:
        mail = fake_mail.next_sibling.next_sibling.get_text().strip().replace(" ",
                                                                              "")  # gets the email from the contact informations and removes the empty spaces from the obtained string

    if mail == "-":
        mail = "N/A"
    print(mail)
    fake_website = c.findAll("div", {"class", "block"})[1].find("i", {"class",
                                                                      "fas fa-globe"})  # variable representing the website regardless if it exists or not

    if fake_website != None:
        website = fake_website.next_sibling.next_sibling.get_text()  # gets the email from the contact informations

    print(website)
    res["phone"] = [phone]
    res["fax"] = fax
    res["mail"] = mail
    res["website"] = website
    return res
