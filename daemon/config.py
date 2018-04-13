import os
import configparser
import logging

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
            raise Exception("File 'config.cfg' does not exist.")

        self.config = {
            'daemon': {
                'timeout': DEFAULT_TIMEOUT
            },
            'mail': {
                'enabled': False
            },
            'logging': {
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
        if config.has_option('notifier', 'type'):
            self.config['notifier']['type'] = config.get('notifier', 'type')

        # log
        if config.has_option('logging', 'path'):
            self.config['logging']['path'] = config.get('logging', 'path')            
        if config.has_option('logging', 'level'):
            self.config['logging']['level'] = int(config.get('logging', 'level'))


    def __getitem__(self, attr):
        """Dictionary interface. Only getter"""
        return self.config[attr]
