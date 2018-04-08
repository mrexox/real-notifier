import os

class Notifier():    
    def notify(self, message):
        """All notifiers must realize this method"""
        raise NotImplementedError("Should implement your own notifier!")
