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
    guild_id = ''
    guild_name = ''
    # Filter out dm
    if message.guild is None:
        guild_id = '-1'
        guild_name = 'direct-message'
    else:
        guild_id = str(message.guild.id)
        guild_name = str(message.guild.name)
    
    author = message.author
    
    print(f'[{guild_name}] #{message.channel} - ({author}[{author.is_on_mobile()}/{author.bot}]): {message.content}')
    
    server = get_server(guild_id, guild_name)
    channel = get_channel(server, message)

    # If guild.name is not the same as last guild.name, insert new row
    if server.server_name != guild_name:
        ServerModel.create(server=guild_id, server_name=message.guild.name)
    
    MessageModel.create(author=str(author), is_on_mobile=author.is_on_mobile(), is_bot=author.bot, message_content=message.content, channel_id=channel.channel_id)

def get_channel(server, message):
    try:
        channel = ChannelModel.select().where(
            (ChannelModel.server_id == server.server_id) &
            (ChannelModel.channel == message.guild.id) &
            (ChannelModel.channel_name == message.guild.name)
            ).get()
        return channel
    except DoesNotExist:
        channel, _ = ChannelModel.get_or_create(channel=message.channel.id, channel_name=message.channel, server_id=server.server_id)
        return channel
    except Exception as e:
        logging.critical(f'get_channel: {e}')

def get_server(guild_id, guild_name):
    server, created = ServerModel.get_or_create(server=guild_id, server_name=guild_name)
    if created is False:
        ServerModel.update(last_used=datetime.datetime.now()).where(
            (ServerModel.server_id == server.server_id) &
            (ServerModel.server_name == server.server_name)
        ).execute()
    return server

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