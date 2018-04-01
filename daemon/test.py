import sys
# Not forever but for now
sys.path.append("./imap")
sys.path.append("./notifier")

import imap
import notifier

from daemon import Daemon
from config import Config

if __name__ == '__main__':
    config = Config()

    imap = Imap(config.mailLogin, config.mailPassword)

    out = FileNotifier()

    i = 10
    while i:
            out.notify(imap.new_messages_count())
            time.sleep(config.daemonTimeout)
            i = i - 1
