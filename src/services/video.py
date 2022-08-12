# Libs
from datetime import datetime

# Models migrations
from src.models.video import VideoModel
from src.settings.database import conn

def getVideosByChannel(id):
    list = []
    conec = conn.execute(VideoModel.select().where(VideoModel.c.channelId == id)).all()
    for publication in conec:
            list.append(publication._asdict())
    return list

def getVideosById(id):
    return conn.execute(VideoModel.select().where(VideoModel.c.id == id)).first()

def getVideosDays(days: int):
    list = []
    try:
        current_time = datetime.utcnow()
        timeago = current_time - datetime.timedelta(days=days)
        print(timeago)
        conec =  conn.execute(
            VideoModel.select().where(
                VideoModel.c.publishedAt > timeago
            )
        ).all()

        for publication in conec:
            list.append(publication._asdict())

    except ValueError:
        print(ValueError)
        print("ERROR: [src.services: video] - Error ocurred in find videos with date after "+str(timeago))
        list = []

    return list

def updateVideo(video, id: str):
    return conn.execute(
        VideoModel.update()
        .values(video)
        .where(VideoModel.c.id == id)
    )

def createVideo(video):
    return conn.execute(VideoModel.insert().values(video))

def getVideoByChannelName(channel: str):
    list = []
    try:
        consult = None
        consult = VideoModel.select().where(
          VideoModel.c.channelTitle == channel   
        )
            
        conec =  conn.execute(
            consult
        ).all()

        for publication in conec:
            list.append(publication._asdict())

    except ValueError:
        print(ValueError)
        print("ERROR: [src.services: video] - Error ocurred in find videos of channel name "+channel)
        list = []

    return list

