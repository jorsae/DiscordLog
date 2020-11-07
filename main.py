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
    print(f'[{message.guild.name}] #{message.channel} - ({message.author}[{message.author.bot}]): {message.content}')
    
    server, created = ServerModel.get_or_create(server=message.guild.name)
    channel, created = ChannelModel.get_or_create(channel=message.channel, server_id=server.server_id)
    
    """
        message_id = PrimaryKeyField()
        author = TextField()
        is_bot = BooleanField(default=False)
        message_content = TextField()
        created_date = DateTimeField(default=datetime.datetime.now)
        channel_id = ForeignKeyField(ChannelModel, to_field='channel_id')
    """
    table_name = f'{server.server_id}_{message.channel}'.replace('-', '_')
    message_table = type(table_name, (MessageModel,), {})
    database.create_tables([message_table])
    insert_message(table_name, str(message.author), message.author.bot, message.content, message.created_at, channel.channel_id)

def insert_message(table_name, author, is_bot, content, created_at, channel_id):
    query = f"""INSERT INTO '{table_name}' (author, is_bot, message_content, created_date, channel_id)
                VALUES (?, ?, ?, ?, ?)"""
    values = (author, is_bot, content, created_at, channel_id, )
    print(query)
    print(values)
    database.execute_sql(query, values)

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