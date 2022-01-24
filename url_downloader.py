from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--enable-javascript")
    # options.add_argument("--headless")
    options.add_argument("window-size=1920x1080")
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    return driver