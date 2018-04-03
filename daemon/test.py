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
        imap = Imap(config.mailLogin, config.mailPassword)
    except ImapException:
        print("exception!")

    if config.notifyType == "file":
        out = FileNotifier()

    i = 5
    while i:
            out.notify(str(imap.new_messages_count()))
            time.sleep(int(config.daemonTimeout))
            i = i - 1
