import imaplib
import getpass

imap = imaplib.IMAP4_SSL('imap.mail.ru')
print(imap.login('your@mail.ru', getpass.getpass()))
print(imap.select('INBOX'))
print(imap.search(None, '(UNSEEN)'))
