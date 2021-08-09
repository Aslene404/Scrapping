from selenium import webdriver


def configure_driver():
    """configure driver on local"""
    options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=r"C:/webdriver/chromedriver.exe", options=options)
    return driver


if __name__ == "__main__":
    configure_driver()
