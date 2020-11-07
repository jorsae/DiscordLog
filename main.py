from peewee import *
import settings

from BaseModel import BaseModel, database
from DiscordChannel import DiscordChannel

settings = settings.Settings('settings.json')

def main():
    tt = type('test_table', (DiscordChannel,), {})
    database.create_tables([tt])


def setup_logging():
    logFolder = 'logs'
    logFile = 'discordLog.log'
    if not os.path.isdir(logFolder):
        os.makedirs(logFolder)

    logging.basicConfig(filename=f'{logFolder}/{logFile}', level=logging.INFO, format='%(asctime)s %(levelname)s:[%(filename)s:%(lineno)d] %(message)s')

if __name__ == '__main__':
    settings.parse_settings()
    settings.print_settings()

    main()