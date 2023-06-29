class Device:
    """Device container class"""
    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url

    @property
    def props(self):
        return self.__dict__