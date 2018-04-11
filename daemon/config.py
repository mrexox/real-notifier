import os
import configparser

DEFAULT_TIMEOUT = 60
DEFAULT_LOGLEVEL = 20
DEFAULT_LOGPATH = "/tmp"
DEFAULT_NOTIFY_TYPE = "file"


class Config:
    """Provides access to parameters in config.cfg"""
    
    def __init__(self):
        config = configparser.ConfigParser()
        if os.path.exists("config.cfg"): # (ian) I suggest to put it to /etc/rnotifier/config.ini
            config.read("config.cfg")
        else:
            print("File 'config.cfg' does not exist")
            raise Exception() # TODO specify exception

        self.config = {
            'daemon': {
                'timeout': DEFAULT_TIMEOUT
            },
            'mail': {
                'enabled': False
            },
            'log': {
                'path': DEFAULT_LOGPATH,
                'level': DEFAULT_LOGLEVEL
            },
            'notifier': {
                'type': DEFAULT_NOTIFY_TYPE
            }
        }
        
        # daemon
        if config.has_option('daemon', 'timeout'):
            self.config['daemon']['timeout'] = int(config.get('daemon', 'timeout'))

        # imap
        if config.has_option('imap', 'login') and config.has_option('imap', 'password'):
            # !Check if empty
            self.config['mail']['enabled'] = True
            self.config['mail']['login'] = config.get('imap', 'login')
            self.config['mail']['password'] = config.get('imap', 'password')

        # notify
        if config.has_option('notify', 'type'):
            self.config['notify']['type'] = config.get('notify', 'type')

        # log
        if config.has_option('log', 'path'):
            self.config['log']['path'] = config.get('log', 'path')
            
        if config.has_option('log', 'level'):
            self.config['log']['level'] = int(config.get('log', 'level'))

    def __getitem__(self, attr):
        """Dictionary interface. Only getter"""
        return self.config[attr]
