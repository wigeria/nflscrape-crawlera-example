from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from shutil import which
import time
import os


class NFLScraper:
    """ A Base class that provides all of the generic code for the scrapers
        The provider-specific scraper classes all inherit from this
    """
    # Base Settings for the login steps
    LOGIN_URL = "https://www.nfl.com/login"
    EMAIL_XPATH = "//input[@id='fanProfileEmailUsername']"
    PASSWORD_XPATH = "//input[@id='fanProfilePassword']"
    LOGIN_BUTTON_XPATH = "//button[@data-test-id='fanProfileSigninButton']"
    LOGGED_IN_ELEMENT = "//a[@href='/account/edit-profile']"

    element_wait_time = 5 # general wait time for most elements' appearance/clickability

    def __init__(self, use_proxy=False, headless=True):
        """ Initializes PhantomJS driver and sets it as a class property """
        # Getting the chromedriver path from the directories in PATH
        CHROMEDRIVER_PATH = which("chromedriver")
        capabilities = dict(DesiredCapabilities.CHROME)
        options = webdriver.ChromeOptions()
        options.add_argument("log-level=2")

        # disable images to speed up the page loading
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        # Adding the headless argument if required
        if headless:
            options.add_argument("--headless")
            options.add_argument("disable-gpu")
        # Options for running through gunicorn ()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')

        if use_proxy:
            # Setting up the proxy
            CRAWLERA_HEADLESS_PROXY = "localhost:3128"

            proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': CRAWLERA_HEADLESS_PROXY,
                'ftpProxy' : CRAWLERA_HEADLESS_PROXY,
                'sslProxy' : CRAWLERA_HEADLESS_PROXY,
                'noProxy'  : ''
            })

            proxy.add_to_capabilities(capabilities)

        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options, desired_capabilities=capabilities)

    def is_logged_in(self):
        """ Checks whether the user is logged in or not """
        cookies = self.driver.get_cookies()

        for cookie in cookies:
            # Return True if the userId cookie isn't undefined, otherwise return False
            if cookie["domain"] == ".nfl.com" and cookie["name"] == "userId" and cookie["value"] != "undefined":
                return True
        return False

    def login(self, email="", password=""):
        """ Logs into the provider site with the provided credentials
            This is defined in the base class because the login process is generally
            very straight forward - type in the credentials, click on a button, wait and confirm
        """
        assert email and password

        if self.is_logged_in():
            return True

        # Navigating to the login page
        self.driver.get(self.LOGIN_URL)

        # Submitting the login form
        self.driver.find_element_by_xpath(self.EMAIL_XPATH).send_keys(email)
        self.driver.find_element_by_xpath(self.PASSWORD_XPATH).send_keys(password)
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON_XPATH).click()
        # Waiting for the login to finish - Ignore the exception since it just means the user didn't get 
        #   logged in
        try:
            WebDriverWait(self.driver, self.element_wait_time).until(EC.presence_of_element_located((By.XPATH,
                self.LOGGED_IN_ELEMENT)))
        except:
            pass

        # Confirming that the user was logged in
        if not self.is_logged_in():
            raise InvalidCredentialsError((email, password,), "Unable to login to NFL.")
        return True


if __name__ == "__main__":
    scraper = NFLScraper(use_proxy=True, headless=False)
    print(scraper.login(email=os.environ.get("NFL_EMAIL"), password=os.environ.get("NFL_PASS")))


