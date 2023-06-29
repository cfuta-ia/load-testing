from framework.webdriver import WebDriver
from framework.gateway import IgnitionGateway

URL = 'http://localhost:8088/data/perspective/client/ToastNotification'
webdriver = WebDriver(URL)
#webdriver.configure(URL)

webdriver.add_session()
webdriver.add_session()
#webdriver.shutdown()

print(webdriver.driver)