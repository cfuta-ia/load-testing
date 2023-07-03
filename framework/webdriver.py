from selenium.webdriver import Firefox, FirefoxProfile
from .gateway import IgnitionGateway
from .util import config

class WebDriver(object):
    """Client"""
    WAIT_TIME = 1 # wait time for actions -- switching windows etc
    def __init__(self, url):
        self.drivers = []
        self.device = IgnitionGateway(url)
        self.count = {'value': 0, 'max': 0}

    def set_device(self, url):
        """Sets the url for the webdriver to access
        
        Args:
            url: url the webdriver sessions will be pointed to
        Returns:
            None
        """
        self.device = IgnitionGateway(url)
        return None
    
    def clear_device(self):
        """Clears the device from the webdriver"""
        del self.device
        self.device = None
        return None

    def add_session(self):
        """ """
        if bool(self.device):
            driver = Firefox(**config.getWebDriverArgs())
            driver.get(self.device.url)
            self.drivers.append(driver)
            self.setCount()
        return None
    
    def remove_session(self):
        """ """
        if len(self.drivers) > 0 and bool(self.device):
            self.drivers[-1].close()
            self.drivers[-1].quit()
            del self.drivers[-1]
        self.setCount()
        return None

    def shutdown(self):
        """End the browser session"""
        if bool(self.drivers) and len(self.drivers) > 0:
            for idx in range(len(self.drivers)):
                self.drivers[-1].close()
                self.drivers[-1].quit()
                del self.drivers[-1]
        return None

    def setCount(self):
        """ """
        self.count['value'] = len(self.drivers)
        if self.count['value'] > self.count['max']:
            self.count['max'] = self.count['value']
        return None
    
    @property
    def currentCount(self):
        return self.count['value']
    
    @property
    def maxCount(self):
        return self.count['max']