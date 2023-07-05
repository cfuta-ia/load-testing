from selenium.webdriver import Firefox
from .gateway import IgnitionGateway
from .util import logger
from .util.config import WebDriverConfig
from datetime import datetime

class WebDriver(object):
    """Client"""
    def __init__(self):
        self.initialConditions()

    def initialConditions(self):
        """ """
        self.drivers = []
        self.device = None
        self.filename = None
        self.count = {'value': 0, 'max': 0}

    def reset(self):
        """Clears the device from the webdriver"""
        del self.device, self.drivers, self.filename, self.count
        self.initialConditions()
        return None

    def configure(self, url):
        """Sets the url for the webdriver to access
        
        Args:
            url: url the webdriver sessions will be pointed to
        Returns:
            None
        """
        if not bool(self.device):
            self.device = IgnitionGateway(url)
            self.filename = logger.createCSV()
        return None

    def addSession(self):
        """ """
        if self.isConfigured:
            driver = Firefox(**WebDriverConfig())
            driver.get(self.device.url)
            self.drivers.append(driver)
            self.setCount()
            self.fileWrite()
        return None
    
    def removeSession(self, index=-1):
        """ """
        if self.isConfigured and len(self.drivers) > 0:
            self.drivers[index].close()
            self.drivers[index].quit()
            del self.drivers[index]
            self.setCount()
            self.fileWrite()
        return None

    def shutdown(self):
        """End the browser session"""
        while len(self.drivers) > 0:
            self.removeSession()
        self.reset()
        return None

    def setCount(self):
        """ """
        self.count['value'] = len(self.drivers)
        if self.count['value'] > self.count['max']:
            self.count['max'] = self.count['value']
        return None
    
    def fileWrite(self):
        """ """
        logger.writeTo(self.filename, *(self.currentCount, self.maxCount, datetime.now()))
        return None
    
    @property
    def currentCount(self):
        return self.count['value']
    
    @property
    def maxCount(self):
        return self.count['max']
    
    @property
    def isConfigured(self):
        """ """
        return bool(self.device)