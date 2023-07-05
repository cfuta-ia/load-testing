from datetime import datetime

class Response:
    """API response container"""
    def __init__(self, message=None, **kwargs):
        self.message = message
        self.timestamp = datetime.now()
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def props(self):
        """Return the properties of this class as a dictionary"""
        return self.__dict__