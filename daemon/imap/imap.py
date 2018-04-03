import imaplib

from imapException import ImapException

# Я думаю, что нужно отлавливать исключения этого класса в демоне
# Исключение может появиться в случае создания объекта и вызова
# метода new_messages_count

class Imap():
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

    def new_messages_count(self):
        (status, messages) = self.imap.search(None, '(UNSEEN)')
            
        if status == 'OK':
            return len(messages[0].split(b' '))
        else:
            raise ImapException("bad response from mail server")