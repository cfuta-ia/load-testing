from .util.device import Device

class IgnitionGateway(Device):
    """Igntion gateway device
    
    Args:
       url: url to the perspective project you will be testing in the webdriver
    """
    def __init__(self, url):
        Device.__init__(self, 'device-gateway', None, url)

