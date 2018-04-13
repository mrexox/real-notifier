import sys
import time
import logging

sys.path.append("./monitor/imap")
sys.path.append("./notifier")
from daemon import Daemon
from config import Config
from imap import Imap, ImapException
from notifier.file import FileNotifier

class NotifierDaemon(Daemon):
    def _run(self):
        monitors = list()
        out = False

        # Init all monitors
        if self.config['mail']['enabled']:
            try:
                imap = Imap(self.config['mail']['login'], self.config['mail']['password'])
            except ImapException as e:
                logging.error(e)
            else:
                monitors.append(imap)
                logging.debug("NotifierDaemon: All monitors initialized succesful")
                
        
        # Init notifier
        try:
            if self.config['notifier']['type'] == "file":
                out = FileNotifier()
                logging.debug("NotifierDaemon: FileNotifier initialized succesful")
            elif self.config['notifier']['type'] == "serial":
                out = SerialNotifier()
                logging.debug("NotifierDaemon: SerialNotifier initialized succesful")
        except Exception as e:
            logging.error("NotifierDaemon can't notify ({0})".format(e))
        

        while True:
            for monitor in monitors:
                # Try get updates from monitors
                try:
                    count = str(monitor.messages_count())
                except ImapException as e:
                    logging.error(e)
                else:
                    logging.debug("get new messages count from " + type(monitor).__name__ + " = " + count)

                # Notifying about updates
                try:
                    out.notify(count)
                except Exception as e:
                    logging.error(e)

            time.sleep(self.config['daemon']['timeout'])


# ---- Testing ----

if __name__ == '__main__':
    import tempfile
    
    pid_file = tempfile.gettempdir() + '/daemonRealNotifier.pid'
    daemon = NotifierDaemon(pid_file)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print('Unknown command')
            sys.exit(2)
        sys.exit(0)
    else:
        print('usage: %s start\nstop\nrestart' % sys.argv[0])
        sys.exit(2)
