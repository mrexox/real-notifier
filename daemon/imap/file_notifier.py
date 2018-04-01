import os
import time
from notifier import Notifier
from tempfile import mkstemp

class FileNotifier(Notifier):
    def __init__(self):
        """Creating temporary file with standard function"""
        (handle, path) = mkstemp(suffix='notifications')
        self.tmpfile = handle
        self.tmpfilename = path
        
    def notify(self, message):
        """The interface method realization.
        Returns:
            True - if the write operation was successful.
            None - otherwise
        """
        bytes_written = os.write(self.tmpfile, str.encode(message)) # expects bytes
        if bytes_written == len(message):
            self.log(message)
            return True

    def log(self, message):
        """Logger, for us to see what happened"""
        print(self.tmpfilename + ": written - " + message)

    def __del__(self):
        """Cleaning after"""
        os.close(self.tmpfile)
        os.remove(self.tmpfilename)

# Testing
if __name__ == '__main__':
    notifier = FileNotifier()
    for mes in ['Hello',
                'Hi',
                'How are you?',
                'I am fine']:
        notifier.notify(mes)
        time.sleep(3)

