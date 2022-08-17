# Models migrations
from src.models.topics import TopicsModel
from src.settings.database import conn

def getActiveTopics():
    list = []
    try:
        conec  = conn.execute(TopicsModel.select().where(TopicsModel.c.active == True)).all()
        
        for publication in conec:
            list.append(publication._asdict())

    except ValueError:
        print(ValueError)
        print("ERROR: [src.services: targets] - Error ocurred in find active targets")
        list = []

    return list