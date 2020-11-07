from peewee import *
import datetime
from BaseModel import BaseModel
from ServerModel import ServerModel

class ChannelModel(BaseModel):
    channel_id = PrimaryKeyField()
    channel = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    server_id = ForeignKeyField(ServerModel, to_field="server_id")
    class Meta:
        indexes = (
            (("channel", "server_id"), True),
        )
        db_table = 'Channels'