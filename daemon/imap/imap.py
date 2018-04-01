import imaplib
import getpass

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
        if service not in ['mail.ru', 'yandex.ru']:
            print("Not supported service")
            raise Exception() # TODO specify exception
        
        self.imap = imaplib.IMAP4_SSL('imap.' + service)

        try:
            self.imap.login(login, password)
        except:
            print("Not valid credentials") # TODO log it
            exit(1)

        self.imap.select('INBOX')

    def new_messages_count(self):
        (status, messages) = self.imap.search(None, '(UNSEEN)')
            
        if status == 'OK':
            return len(messages[0].split(b' '))
        else:
            return -1 # raise ImapBadResponseException()
    

if __name__ == '__main__':
    import getpass
    
    imap = Imap('meexox@mail.ru', getpass.getpass())
    print(imap.new_messages_count())
