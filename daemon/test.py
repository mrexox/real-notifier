import sys
# Not forever but for now
sys.path.append("./imap")
sys.path.append("./notifier")

import imap
import notifier

if __name__ == '__main__':
    print(imap.__file__)
