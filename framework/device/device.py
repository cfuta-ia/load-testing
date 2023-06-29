import yaml
from os.path import dirname, join

class Device:
    """Client class"""
    FILE_KEYS = {'name', 'description', 'url'}
    FILE_TYPE = '.yaml'
    def __init__(self, filename):
        self.loadConfig(filename)

    def loadConfig(self, filename):
        """Load the config for the client from the client-configs directory"""
        path = join(dirname(__file__), 'configs', filename + self.FILE_TYPE)
        print(path)
        try:
            with open(path, 'r') as file:
                config = yaml.safe_load(file)
        except FileNotFoundError:
            config = {}

        for key in self.FILE_KEYS:
            setattr(self, key, config.get(key))

    @property
    def props(self):
        return self.__dict__