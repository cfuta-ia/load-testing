from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def WebDriverConfig(headless=True):
    """ """
    service = Service(GeckoDriverManager().install())
    options = FirefoxOptions()
    options.headless = headless
    return {'service': service, 'options': options}

def FlaskConfig(host='0.0.0.0', port=5000, debug=False):
    """ """
    return {'host': host, 'port': port, 'debug': debug}