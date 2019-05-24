from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from shutil import which
import time
import os
from scraper import Scraper


class NFLScraper(Scraper):
    """ A Base class that provides all of the generic code for the scrapers
        The provider-specific scraper classes all inherit from this
    """
    # Base Settings for the login steps
    LOGIN_URL = "https://www.nfl.com/login"
    EMAIL_XPATH = "//input[@id='fanProfileEmailUsername']"
    PASSWORD_XPATH = "//input[@id='fanProfilePassword']"
    LOGIN_BUTTON_XPATH = "//button[@data-test-id='fanProfileSigninButton']"
    LOGGED_IN_ELEMENT = "//div[@data-test-id='user-tile--wrapper']"

    def is_logged_in(self):
        """ Checks whether the user is logged in or not """
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,
                self.LOGGED_IN_ELEMENT)))
            return True
        except:
            return False
        

if __name__ == "__main__":
    scraper = NFLScraper(use_proxy=True, headless=True)
    print(scraper.login(email=os.environ.get("NFL_EMAIL"), password=os.environ.get("NFL_PASS")))


