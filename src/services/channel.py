# Libs
from datetime import datetime

# Models migrations
from src.models.channel import ChannelModel
from src.settings.database import conn

def getChannelById(id):
    return conn.execute(ChannelModel.select().where(ChannelModel.c.id == id)).first()

def updateChannel(channel, id: str):
    return conn.execute(
        ChannelModel.update()
        .values(channel)
        .where(ChannelModel.c.id == id)
    )

def createChannel(channel):
    return conn.execute(ChannelModel.insert().values(channel))

def getChannelByName(channel: str):
    list = []
    try:
        consult = None
        consult = ChannelModel.select().where(
          ChannelModel.c.title == channel   
        )
            
        conec =  conn.execute(
            consult
        ).first()

        for publication in conec:
            list.append(publication._asdict())

    except ValueError:
        print(ValueError)
        print("ERROR: [src.services: Channel] - Error ocurred in find channel by name "+channel)
        list = []

    return list

