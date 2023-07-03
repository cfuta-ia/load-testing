from framework.webdriver import WebDriver
from selenium.webdriver import FirefoxOptions, FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from selenium.webdriver import Firefox
from framework.util import config

URL = "https://ignitionbuildathon.com/data/perspective/client/BAT-2023-Leaderboard/load-test"
args = config.get('webdriver')
#args['options']._profile = FirefoxProfile()

driver = Firefox(**config.getWebDriverArgs())
driver.get(URL)


#args['options']._profile = FirefoxProfile()
driver1 = Firefox(**config.getWebDriverArgs())
driver1.get(URL)
driver.close()
driver.quit()



#d1 = WebDriver(URL)
#d2 = WebDriver(URL)


#d1.add_session()
#d2.add_session()