def deep_info_extraction(c, res):
    """extracts more information from each page """
    info = c.findAll("div", {"class": "col-sm-12"})  # gets the div containing contact information
    for i in info:
        name = i.find("strong").get_text()
        print(name)
        street = i.findAll("br")[0].next_sibling.strip()
        print(street)
        city = i.findAll("br")[1].next_sibling.strip()
        print(city)
        phone = i.findAll("br")[2].next_sibling.strip().replace("Telefon: ",
                                                                "")  # gets the phone number from the contact informations and removes the Telefon: from the obtained string

        if phone == "":
            phone = "N/A"
        print(phone)
        website = i.find("a")['href']  # gets all the links in the info section
        if website[0] != "h":  # checks if the retrieved link is a website address
            website = "N/A"
        print(website)
        res = {
            'name': name,
            'street': street,
            'city': city,
            'branche': 'health',
            'category': 'clinics',
            'phone': [phone],
            'website': website}
    return res


def bed_info_extraction(soup, res):
    """extracts bed numbers info from dedicated section"""
    bed_numbers = soup.findAll("div", {
        "class": "col-sm-4 col-xs-12 rowtable-title hyphenate"})  # gets the div containin information about the number of beds and annual cases
    number_of_beds = bed_numbers[1].get_text().strip()
    number_of_annual_cases = bed_numbers[3].get_text().strip()
    print(number_of_beds)
    print(number_of_annual_cases)

    res["number_of_beds"] = number_of_beds
    res["number_of_annual_cases"] = number_of_annual_cases
    print(res)
    return res
