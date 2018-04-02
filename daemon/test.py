import sys
# Not forever but for now
sys.path.append("./imap")
sys.path.append("./notifier")

from  imap.imap import Imap
from notifier.file import FileNotifier

from daemon import Daemon
from config import Config

if __name__ == '__main__':
    import time # for sleep
    config = Config()

    im = Imap(config.mailLogin, config.mailPassword)

    out = FileNotifier()

    i = 10
    while i:
            out.notify(str(im.new_messages_count()))
            time.sleep(int(config.daemonTimeout))
            i = i - 1
