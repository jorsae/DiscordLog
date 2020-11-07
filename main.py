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
    
    server = get_server(message)
    channel = get_channel(server, message)

    # If guild.name is not the same as last guild.name, insert new row
    if server.server_name != message.guild.name:
        ServerModel.create(server=str(message.guild.id), server_name=message.guild.name)
    
    MessageModel.create(author=str(message.author), is_bot=message.author.bot, message_content=message.content, channel_id=channel.channel_id)

def get_channel(server, message):
    try:
        channel = ChannelModel.select().where(ChannelModel.server_id == server.server_id, ChannelModel.channel_name == server.server_name).get()
        return channel
    except DoesNotExist:
        channel, _ = ChannelModel.get_or_create(channel=message.channel.id, channel_name=message.channel, server_id=server.server_id)
        logging.info(f'New channel: {message.channel} added')
        return channel
    except Exception as e:
        logging.critical(f'get_channel: {e}')

def get_server(message):
    try:
        server = ServerModel.select().where(ServerModel.server == str(message.guild.id)).order_by(ServerModel.created_date.desc()).get()
        return server
    except DoesNotExist:
        server, _ = ServerModel.get_or_create(server=str(message.guild.id), server_name=message.guild.name)
        logging.info(f'New server: ({server.server_id}) {server.server} added')
        return server
    except Exception as e:
        logging.critical(f'get_server: {e}')

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