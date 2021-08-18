def info_extraction(d,res):
    """extract information from the main page """
    name_ex = d.findAll("strong")
    for n in name_ex:
        name = n.get_text()
        print(name)

        first_name = name.split()[0]
        print(first_name)
        last_name = name.split(' ', 1)[1]
        print(last_name)

        phone_mail = d.findAll("a")
        if len(phone_mail) == 2:
            phone = phone_mail[0].get_text().strip().replace("Telefon: ", "")
            mail = phone_mail[1].get_text().strip().replace("E-Mail: ", "")
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
def service_extraction(d,data):
    """extract information about the services provided by the midwife """
    serv = d.findAll("span", {"class": "sr-only"})

    for s in serv:

        if s.get_text() == ": Ja":
            data.append(True)
        else:
            data.append(False)
    return data
