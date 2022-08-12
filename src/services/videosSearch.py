# Libs
from datetime import datetime

# Models migrations
from src.models.videoSearch import VideoSearchModel
from src.settings.database import conn

def getVideosSearchByChannel(id):
    list = []
    conec = conn.execute(VideoSearchModel.select().where(VideoSearchModel.c.channelId == id)).all()
    for publication in conec:
            list.append(publication._asdict())
    return list

def getVideosSearchById(id):
    return conn.execute(VideoSearchModel.select().where(VideoSearchModel.c.id == id)).first()

def getVideosSearchDays(days: int):
    list = []
    try:
        current_time = datetime.utcnow()
        timeago = current_time - datetime.timedelta(days=days)
        print(timeago)
        conec =  conn.execute(
            VideoSearchModel.select().where(
                VideoSearchModel.c.publishedAt > timeago
            )
        ).all()

        for publication in conec:
            list.append(publication._asdict())

    except ValueError:
        print(ValueError)
        print("ERROR: [src.services: video] - Error ocurred in find videos with date after "+str(timeago))
        list = []

    return list

def updateVideoSearch(video, id: str):
    return conn.execute(
        VideoSearchModel.update()
        .values(video)
        .where(VideoSearchModel.c.id == id)
    )

def createVideoSearch(video):
    return conn.execute(VideoSearchModel.insert().values(video))

def getVideoSearchByChannelName(channel: str):
    list = []
    try:
        consult = None
        consult = VideoSearchModel.select().where(
          VideoSearchModel.c.channelTitle == channel   
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

