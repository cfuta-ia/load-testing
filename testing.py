from framework.webdriver.webdriver import WebDriver
from framework.device.device import Device

webdriver = WebDriver()
device = Device('test')

webdriver.add_session(device.url, False)
webdriver.add_session(device.url)
webdriver.shutdown()

print(webdriver.driver)