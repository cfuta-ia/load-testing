from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

SERVICE = Service(GeckoDriverManager().install())
OPTIONS = FirefoxOptions()
OPTIONS.headless = False

def getWebDriverArgs(headless=True):
    """ """
    service = Service(GeckoDriverManager().install())
    options = FirefoxOptions()
    options.headless = headless
    #options._profile = FirefoxProfile()
    return {'service': service, 'options': options}

HOST = '0.0.0.0'
PORT = 5000
DEBUG = False

def get(config):
    """Return the config dictionary from the above values"""
    config = config.lower()
    if config == 'webdriver':
        return {'service': SERVICE, 'options': OPTIONS}
    elif config == 'app':
        return {'host': HOST, 'port': PORT, 'debug': DEBUG}
    else:
        return {}