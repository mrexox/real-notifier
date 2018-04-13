import sys
import time
import logging

sys.path.append("./imap")
sys.path.append("./notifier")
from daemon import Daemon
from config import Config
from imap.imap import *
from notifier.file import FileNotifier

class NotifierDaemon(Daemon):
    def _run(self):
        imap = False
        out = False

        if self.config['mail']['enabled']:
            try:
                imap = Imap(self.config['mail']['login'], self.config['mail']['password'])
            except ImapException as e:
                logging.error(e)
            else:
                logging.debug("RealNotifier: Imap initialized")        

        if self.config['notifier']['type'] == "file":
            out = FileNotifier()
            logging.debug("RealNotifier: FileNotifier initialized")
        # elif config.notifyType == "oter notify type":
        #     out = OtherNotifier()

        while True:
            if imap:
                try:
                    imap_count = str(imap.new_messages_count())
                except ImapException as e:
                    logging.error(e)
                else:
                    logging.debug("new messages count from imap = {0}".format(imap_count))
                    
            try:
                out.notify(imap_count)
                time.sleep(self.config['daemon']['timeout'])
            except Exception as e:
                logging.error(e)
                sys.exit(1)


# ---- Testing ----

if __name__ == '__main__':
    import tempfile
    
    pid_file = tempfile.gettempdir() + '/daemonRealNotifier.pid'
    daemon = NotifierDaemon(pid_file)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
            print('Daemon started!')
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            print('Daemon stopped!')
        elif 'restart' == sys.argv[1]:
            daemon.restart()
            print('Daemon restarted!')
        else:
            print('Unknown command')
            sys.exit(2)
        sys.exit(0)
    else:
        print('usage: %s start|stop|restart' % sys.argv[0])
        sys.exit(2)
