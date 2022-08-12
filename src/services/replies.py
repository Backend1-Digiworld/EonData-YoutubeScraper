# Libs
from datetime import datetime

# Models migrations
from src.models.replies import RepliesModel
from src.settings.database import conn

def getRepliesByVideo(id):
    list = []
    try:
        conec  = conn.execute(RepliesModel.select().where(RepliesModel.c.videoId == id)).all()
        
        for publication in conec:
            list.append(publication._asdict())

    except ValueError:
        print(ValueError)
        print("ERROR: [src.services: comment] - Error ocurred in find replies of videos "+id)
        list = []

    return list

def getRepliesByComment(id):
    list = []
    try:
        conec  = conn.execute(RepliesModel.select().where(RepliesModel.c.commentId == id)).all()
        
        for publication in conec:
            list.append(publication._asdict())

    except ValueError:
        print(ValueError)
        print("ERROR: [src.services: comment] - Error ocurred in find replies of comment "+id)
        list = []

    return list

def getRepliesById(id):
    return conn.execute(RepliesModel.select().where(RepliesModel.c.id == id)).first()

def updateReplies(replies, id: str):
    return conn.execute(
        RepliesModel.update()
        .values(replies)
        .where(RepliesModel.c.id == id)
    )

def createReplies(replies):
    return conn.execute(RepliesModel.insert().values(replies))
