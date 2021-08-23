def info_extraction(d, res):
    """extract information from the main page """
    name_ex = d.findAll("strong")
    for n in name_ex:
        name = n.get_text()  # gets the full name
        print(name)

        first_name = name.split()[0]  # gets the first name from the full name
        print(first_name)
        last_name = name.split(' ', 1)[1]  # gets the last name from the full name
        print(last_name)

        phone_mail = d.findAll("a")  # gets the phone and mail if each one exists
        if len(phone_mail) == 2:
            phone = phone_mail[0].get_text().strip().replace("Telefon: ",
                                                             "")  # gets the phone number from the contact informations and removes the Telefon: from the obtained string

            mail = phone_mail[1].get_text().strip().replace("E-Mail: ",
                                                            "")  # gets the email from the contact informations and removes the E-mail: from the obtained string

        if len(phone_mail) == 1:
            phone = phone_mail[0].get_text().strip().replace("Telefon: ", "")
            mail = "N/A"
        if len(phone_mail) == 0:
            phone = "N/A"
            mail = "N/A"

        print(phone)

        print(mail)
        res = {
            'branche': 'health',
            'category': 'midwife',
            'salutation': 'Frau',
            'first_name': first_name,
            'last_name': last_name,
            'phone': [phone],
            'mail': mail
        }
    return res


def service_extraction(d, data):
    """extract information about the services provided by the midwife """
    serv = d.findAll("span", {"class": "sr-only"})  # gets all the informations about the services

    for s in serv:

        if s.get_text() == ": Ja":  # if the service is provided insert True in the corresponding array column
            data.append(True)
        else:
            data.append(False)
    return data
