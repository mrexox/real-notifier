import tempfile, os, sys

from daemon import Daemon
from config import Config

sys.path.append("./notifier")

class daemonRealNotifier(Daemon):
    def run(self):
        config = Config()

        if config.mail:
            sys.path.append("./imap")
            import imap
            imap = Imap(config.mailLogin, config.mailPassword)
        
        if config.notifyType == "file":            
            import notifier
            out = FileNotifier()
        #elif config.notifyType == "oter notify type":
        #    out = OtherNotifier()

        while True:
            out.notify(imap.new_messages_count())
            time.sleep(config.daemonTimeout)


if __name__ == '__main__':
    pidFile = tempfile.gettempdir() + '/daemonRealNotifier.pid'
    daemon = daemonRealNotifier(pidFile)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print('Daemon starting..')
            daemon.start()
            print('Daemon started!')
        elif 'stop' == sys.argv[1]:
            print('Daemon stopping..')
            daemon.stop()
            print('Daemon stopped!')
        elif 'restart' == sys.argv[1]:
            print('Daemon restarting..')
            daemon.restart()
            print('Daemon restarted!')
        else:
            print('Unknown command')
            sys.exit(2)
        sys.exit(0)
    else:
        print('usage: %s start|stop|restart' % sys.argv[0])
        sys.exit(2)