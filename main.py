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
    
    if str(message.guild.id) != str(762171368942338083):
        return

    print(f'[{message.guild.name}] #{message.channel} - ({message.author}[{message.author.bot}]): {message.content}')

    try:
        server = ServerModel.select().where(ServerModel.server == str(message.guild.id)).order_by(ServerModel.created_date.desc()).get()
    except DoesNotExist:
        server, _ = ServerModel.get_or_create(server=str(message.guild.id), server_name=message.guild.name)
        logging.info(f'New channel: ({server.server_id}) {server.server} added')
    except Exception as e:
        logging.critical(f'Error when trying to get most recent server: {e}')
    
    # If guild.name is not the same as last guild.name, insert new row
    if server.server_name != message.guild.name:
        ServerModel.create(server=str(message.guild.id), server_name=message.guild.name)
    
    channel, _ = ChannelModel.get_or_create(channel=message.channel, server_id=server.server_id)
    MessageModel.create(author=str(message.author), is_bot=message.author.bot, message_content=message.content, channel_id=channel.channel_id)

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