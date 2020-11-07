from peewee import *
import datetime
from BaseModel import BaseModel

class ServerModel(BaseModel):
    server_id = PrimaryKeyField()
    server = TextField(unique=True)
    created_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'Servers'