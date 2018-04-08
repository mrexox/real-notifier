import logging
import tempfile
from config import Config

config = Config()

logging.basicConfig(filename = config.logPath + '/RealNotirier.log',
                    filemode="w",
                    level = config.logLevel,
                    format = '%(asctime)s %(levelname)s: %(message)s',
                    datefmt = '%Y-%m-%d %I:%M:%S')

logging.info('Daemon start')
logging.debug('Daemon ulala')
logging.error('Daemon error')
