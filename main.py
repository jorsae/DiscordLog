from peewee import *
import discord
import os
import datetime
import logging

import settings
import constants
from BaseModel import BaseModel, database
from ChannelModel import ChannelModel
from ServerModel import ServerModel
from MessageModel import MessageModel

client = discord.Client()
settings = settings.Settings('settings.json')

@client.event
async def on_message(message):
    # Filter out dm
    if message.guild is None:
        return
    
    print(f'[{message.guild.name}] #{message.channel} - ({message.author}[{message.author.bot}]): {message.content}')
    
    server, _ = ServerModel.get_or_create(server=message.guild.name)
    channel, _ = ChannelModel.get_or_create(channel=message.channel, server_id=server.server_id)
    message, _ = MessageModel.get_or_create(author=str(message.author), is_bot=message.author.bot, message_content=message.content, channel_id=channel.channel_id)

def setup_database():
    database.create_tables([ChannelModel, ServerModel, MessageModel])

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