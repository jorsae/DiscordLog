from peewee import *

import settings

settings = settings.Settings('settings.json')


def setup_logging():
    logFolder = 'logs'
    logFile = 'muda.log'
    if not os.path.isdir(logFolder):
        os.makedirs(logFolder)

    logging.basicConfig(filename=f'{logFolder}/{logFile}', level=logging.INFO, format='%(asctime)s %(levelname)s:[%(filename)s:%(lineno)d] %(message)s')

if __name__ == '__main__':
    settings.parse_settings()
    settings.print_settings()