from peewee import *
import settings

database = SqliteDatabase("DiscordLog.db")

class BaseModel(Model):
    class Meta:
        database = database