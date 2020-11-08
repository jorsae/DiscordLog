from peewee import *
import datetime
from BaseModel import BaseModel
from ChannelModel import ChannelModel

class MessageModel(BaseModel):
    message_id = PrimaryKeyField()
    author = TextField()
    is_on_mobile = BooleanField(default=False)
    is_bot = BooleanField(default=False)
    message_content = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    channel_id = ForeignKeyField(ChannelModel, to_field='channel_id')
    
    class Meta:
        db_table = 'Messages'