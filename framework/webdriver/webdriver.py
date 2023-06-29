from selenium.webdriver import Firefox
from .util import config, status
from time import sleep

class WebDriver:
    """Client"""
    WAIT_TIME = 1 # wait time for actions -- switching windows etc
    def __init__(self):
        self.driver = None
        self.device = None

    def startup(self, device):
        """ """
        self.driver = Firefox(**config.get())
        self.device = device

    def add_session(self):
        """ """

    def remove_session(self):
        """ """
        pass

    def shutdown(self):
        """End the browser session"""
        self.driver.close()
        del self.driver
        del self.device
        self.driver = None
        self.device = None
        