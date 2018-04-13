import imaplib
import sys, os

sys.path.append('../../monitor')
from monitor.monitor import Monitor
from imap_exception import ImapException

class Imap(Monitor):
    """Mail communication class
    
    Not fully written yet, so needs:
        Loading configuration
    """

    def __init__(self, login, password):
        service = login.split('@')[1] # split -> ['name', 'service.ru']
        if service not in ['mail.ru', 'yandex.ru', 'yandex.ua']:
            raise ImapException("not supported service")
        
        self.imap = imaplib.IMAP4_SSL('imap.' + service)

        try:
            self.imap.login(login, password)
        except:
            raise ImapException('not valid credentials')

        self.imap.select('INBOX')

    def messages_count(self):
        (status, messages) = self.imap.search(None, '(UNSEEN)')
            
        if status == 'OK':
            return len(messages[0].split(b' '))
        else:
            raise ImapException("bad response from mail server")
