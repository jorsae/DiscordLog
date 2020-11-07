from peewee import *
import datetime

from BaseModel import BaseModel

class DiscordChannel(BaseModel):
    channel_id = PrimaryKeyField()
    author = TextField()
    is_bot = BooleanField(default=False)
    message_content = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
