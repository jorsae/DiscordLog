from peewee import *

import settings

settings = settings.Settings('settings.json')

if __name__ == '__main__':
    settings.parse_settings()
    settings.print_settings()