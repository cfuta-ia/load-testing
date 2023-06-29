from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

SERVICE = Service(GeckoDriverManager().install())
OPTIONS = FirefoxOptions()
OPTIONS.headless = False

def get():
    """Return the config dictionary from the above values"""
    return {'service': SERVICE, 'options': OPTIONS}