def url_construction(company):
    """make the search url using the given company name as keyword and the given company postcode """
    postcode = company["registered_address"].strip()
    postcode = postcode.split(" ")
    for i in range(len(postcode) - 1, 0, -1):  # loop backwards in the obtained string
        if postcode[i].strip().isdigit():  # if the obtained string is fully a number
            postcode = postcode[i].strip()
            break

    keyword = company["name"].strip().replace(" ",
                                              "%20").strip()  # gets the name and replaces empty spaces with "%20" in order to be used as a keyword in the url
    keyword = keyword.replace("&",
                              "%26").strip()  # gets the name and replaces & symbols with "%26" in order to be used as a keyword in the url

    url = "https://www.xing.com/search/companies?zip_code=" + postcode + "&keywords=" + keyword  # making the full url of the search operation
    return url


def info_extraction(r):
    """extracts the needed information about the searched company from the main page"""

    name = r.find("div", {"class": "search-card-style-content-20754fd7"}).findAll("div")[
        0].get_text().strip()  # gets the company name
    print(name)
    address = r.find("div", {"class": "search-card-style-content-20754fd7"}).findAll("div")[
        1].get_text().strip()  # gets the company address
    print(address)
    ort = address.split(",")[0].strip()  # splitting the address with "," and using the first part as ort
    print(ort)
    bundesland = address.split(",")[
        1].strip()  # splitting the address with "," and using the second part as bundeslan
    print(bundesland)
    fake_numbers = r.findAll("span", {
        "class": "CompanyCard-style-minorCopy-b61c6828"})  # variable representing the xing users number and workers number regardless if they exists or not
    if len(fake_numbers) == 0:  # if both numbers are not available
        xing_users = "N/A"
        worker_range = "N/A"
    if len(fake_numbers) == 1 and fake_numbers[
        0].get_text().strip() == "XING members:":  # if only the xing users number is available
        xing_users = fake_numbers[0].next_sibling.strip()
        worker_range = "N/A"
    if len(fake_numbers) == 1 and fake_numbers[
        0].get_text().strip() == "Employees:":  # if only the worker range number is available
        worker_range = fake_numbers[0].next_sibling.strip().replace(" employees",
                                                                    "").strip()  # gets the worker range number and replace " employees" at the end of the obtained string
        xing_users = "N/A"
    if len(fake_numbers) >= 2:
        xing_users = fake_numbers[0].next_sibling.strip()
        worker_range = fake_numbers[1].next_sibling.strip().replace(" employees",
                                                                    "").strip()  # gets the worker range number and replace " employees" at the end of the obtained string

    print(xing_users)
    print(worker_range)
    res = {
        'name': name,
        'ort': ort,
        'bundesland': bundesland,
        'xing_users': xing_users,
        'worker_range': worker_range

    }
    return res
