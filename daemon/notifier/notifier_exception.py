import datetime

class NotifierException(Exception):
    def __init__(self, value):
        self.value = value
        self.timestamp = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
        
    def __str__(self):
        return [repr(self.timestamp), repr(self.value)].join(' ')
