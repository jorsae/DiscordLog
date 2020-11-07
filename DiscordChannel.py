from peewee import *
from BaseModel import BaseModel

class DiscordChannel(BaseModel):
    text = TextField()