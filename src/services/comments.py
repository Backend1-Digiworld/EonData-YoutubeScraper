# Libs
from datetime import datetime

# Models migrations
from src.models.comments import CommentModel
from src.settings.database import conn

def getCommentsByVideo(id):
    list = []
    try:
        conec  = conn.execute(CommentModel.select().where(CommentModel.c.videoId == id)).all()
        
        for publication in conec:
            list.append(publication._asdict())

    except ValueError:
        print(ValueError)
        print("ERROR: [src.services: comment] - Error ocurred in find comments of videos "+id)
        list = []

    return list

def getCommentById(id):
    return conn.execute(CommentModel.select().where(CommentModel.c.id == id)).first()

def updateComment(Comment, id: str):
    return conn.execute(
        CommentModel.update()
        .values(Comment)
        .where(CommentModel.c.id == id)
    )

def createComment(Comment):
    return conn.execute(CommentModel.insert().values(Comment))
