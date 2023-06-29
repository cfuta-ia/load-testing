from selenium.webdriver import Firefox
from .gateway import IgnitionGateway
from .util import config

class WebDriver(object):
    """Client"""
    WAIT_TIME = 1 # wait time for actions -- switching windows etc
    def __init__(self, url):
        self.driver = Firefox(**config.get('webdriver'))
        self.device = IgnitionGateway(url)
        self.count = {'value': 0, 'max': 0}

    def add_session(self):
        """ """
        if self.currentCount != 0:
            self.driver.switch_to.new_window()
        self.driver.get(self.device.url)
        self.focus(-1)
        self.setCount()
        return None
    
    def remove_session(self):
        """ """
        if self.currentCount != 1:
            self.driver.close()
            self.focus()
        self.setCount()
        return None

    def shutdown(self):
        """End the browser session"""
        self.driver.quit()
        return None

    def focus(self, index=-1):
        """Set the driver focus on the tab with the input index"""
        id = self.driver.window_handles[index]
        self.driver.switch_to.window(id)
        return None

    def setCount(self):
        """ """
        self.count['value'] = len(self.driver.window_handles)
        if self.count['value'] > self.count['max']:
            self.count['max'] = self.count['value']
        return None
    
    @property
    def currentCount(self):
        return self.count['value']
    
    @property
    def maxCount(self):
        return self.count['max']