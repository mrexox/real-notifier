import os
import configparser

DEFAULT_TIMEOUT = 60
DEFAULT_LOGLEVEL = 20
DEFAULT_LOGPATH = "/tmp"
DEFAULT_NOTIFY_TYPE = "file"

"""Provides access to parameters in config.cfg"""
class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        if os.path.exists("config.cfg"):
            config.read("config.cfg")
        else:
            print("File 'config.cfg' does not exist")
            raise Exception() # TODO specify exception

        # daemon
        if config.has_option('daemon', 'timeout'):
            self.daemon_timeout = int(config.get('daemon', 'timeout'))
        else:
            self.daemon_timeout = DEFAULT_TIMEOUT

        # imap
        if config.has_option('imap', 'login') and config.has_option('imap', 'password'):
            self.mail = True
            self.mail_login = config.get('imap', 'login')
            self.mail_password = config.get('imap', 'password')
        else:
            self.mail = False

        # notify
        if config.has_option('notify', 'type'):
            self.notify_type = config.get('notify', 'type')
        else:
            self.notify_type = DEFAULT_NOTIFY_TYPE

        # log
        if config.has_option('log', 'path'):
            self.log_path = config.get('log', 'path')
        else:
            self.log_path = DEFAULT_LOGPATH
            
        if config.has_option('log', 'level'):
            self.log_level = int(config.get('log', 'level'))
        else:
            self.log_level = DEFAULT_LOGLEVEL
