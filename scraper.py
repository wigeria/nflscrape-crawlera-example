from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from shutil import which
import time
import os


class Scraper:
    """ A Base class that provides all of the generic code for the scrapers
        The provider-specific scraper classes all inherit from this
    """
    # Base Settings for the login steps
    LOGIN_URL = "" # url to the login page
    EMAIL_XPATH = "" # xpath for the login-email input
    PASSWORD_XPATH = "" # xpath for the login-password input
    LOGIN_BUTTON_XPATH = "" # xpath for the login button
    LOGGED_IN_ELEMENT = "" # xpath for an element that only shows after successful login

    element_wait_time = 20 # general wait time for most elements' appearance/clickability

    
    def __init__(self, use_proxy=False, headless=True):
        """ Initializes the Firefox driver and sets it as a class property """
        profile = webdriver.FirefoxProfile()
        options = webdriver.FirefoxOptions()
        desired_capability = webdriver.DesiredCapabilities.FIREFOX

        if use_proxy:
            CRAWLERA_HEADLESS_PROXY = "localhost:3128"
            desired_capability = webdriver.DesiredCapabilities.FIREFOX
            desired_capability['proxy'] = {
                'proxyType': "manual",
                'httpProxy': CRAWLERA_HEADLESS_PROXY,
                'ftpProxy': CRAWLERA_HEADLESS_PROXY,
                'sslProxy': CRAWLERA_HEADLESS_PROXY,
            }

        if headless:
            options.add_argument("--headless")

        options.add_argument("--window-size 1920,1080")
        self.driver = webdriver.Firefox(options=options, firefox_profile=profile, capabilities=desired_capability)


    def is_logged_in(self):
        """ Checks whether the user is logged in or not """
        raise NotImplementedError("`is_logged_in` must be overridden in Scrapers!")

    def login(self, email="", password=""):
        """ Logs into the provider site with the provided credentials
            This is defined in the base class because the login process is generally
            very straight forward - type in the credentials, click on a button, wait and confirm
        """
        assert email and password

        # Navigating to the login page
        self.driver.get(self.LOGIN_URL)

        # Submitting the login form
        WebDriverWait(self.driver, self.element_wait_time).until(EC.element_to_be_clickable((By.XPATH, self.EMAIL_XPATH)))
        self.driver.find_element_by_xpath(self.EMAIL_XPATH).send_keys(email)
        WebDriverWait(self.driver, self.element_wait_time).until(EC.element_to_be_clickable((By.XPATH, self.PASSWORD_XPATH)))
        self.driver.find_element_by_xpath(self.PASSWORD_XPATH).send_keys(password)

        WebDriverWait(self.driver, self.element_wait_time).until(EC.element_to_be_clickable((By.XPATH, self.LOGIN_BUTTON_XPATH)))
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON_XPATH).click()
        
        # Waiting for the login to finish - Ignore the exception since it just means the user didn't get 
        #   logged in
        try:
            WebDriverWait(self.driver, self.element_wait_time).until(EC.presence_of_element_located((By.XPATH,
                self.LOGGED_IN_ELEMENT)))
        except TimeoutException:
            # Trying clicking the element again in case the first click doesn't work
            try:
                self.driver.find_element_by_xpath(self.LOGIN_BUTTON_XPATH).click()
            except NoSuchElementException: # Meaning that the page is loading
                logged_in = self.is_logged_in() # This also adds a wait

        # Explicit wait before final check
        time.sleep(5)

        # Confirming that the user was logged in
        if not self.is_logged_in():
            raise ValueError("Unable to login.")
        return True
