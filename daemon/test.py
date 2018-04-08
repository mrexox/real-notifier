import sys, time
# Not forever but for now
sys.path.append("./imap")
sys.path.append("./notifier")

from imap.imap import *
from notifier.file import FileNotifier

from config import Config

if __name__ == '__main__':
    config = Config()

    try:
        imap = Imap(config.mail_login, config.mail_password)
    except ImapException:
        print("exception!")

    
    if config.notify_type == "file":
        out = FileNotifier()

    i = 5 # times
    while i:
            out.notify(str(imap.new_messages_count()))
            time.sleep(int(config.daemon_timeout))
            i = i - 1
