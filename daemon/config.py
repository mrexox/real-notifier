import os, configparser

""" Класс организует доступ к параметрам, сохраненным в файле конфигурации config.cfg"""
class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        if os.path.exists("config.cfg"):
            config.read("config.cfg")
        else:
            print("File 'config.cfg' does not exist")
            raise Exception() # TODO specify exception

        if config.has_option('daemon', 'timeout'):
            self.daemonTimeout = config.get('daemon', 'timeout')
        else:
            self.daemonTimeout = 60

        if config.has_option('mail', 'login') and config.has_option('mail', 'password'):
            self.mail = True
            self.mailLogin = config.get('mail', 'login')
            self.mailPassword = config.get('mail', 'password')
        else:
            self.mail = False

        if config.has_option('notify', 'type'):
            self.notifyType = config.get('notify', 'type')
        else:
            self.notifyType = "file"