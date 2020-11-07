from peewee import *
import discord
import os
import logging

import settings
import constants
from BaseModel import BaseModel, database
from ChannelModel import ChannelModel
from ServerModel import ServerModel
from DiscordChannel import DiscordChannel

client = discord.Client()
settings = settings.Settings('settings.json')

@client.event
async def on_message(message):
    print(f'[{message.guild.name}] #{message.channel} - ({message.author}): {message.content}')
    
    server, created = ServerModel.get_or_create(server=message.guild.name)
    channel, created = ChannelModel.get_or_create(channel=message.channel, server_id=server.server_id)

def setup_database():
    database.create_tables([ChannelModel, ServerModel])

def setup_logging():
    logFolder = constants.LOG_FOLDER
    logFile = constants.LOG_FILE
    if not os.path.isdir(logFolder):
        os.makedirs(logFolder)

    logging.basicConfig(filename=f'{logFolder}/{logFile}', level=logging.INFO, format='%(asctime)s %(levelname)s:[%(filename)s:%(lineno)d] %(message)s')

if __name__ == '__main__':
    setup_logging()
    settings.parse_settings()
    settings.print_settings()

    setup_database()

    client.run(settings.token, bot=False)