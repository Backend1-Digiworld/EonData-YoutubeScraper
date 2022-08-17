# Models migrations
from src.models.targets import TargetsModel
from src.settings.database import conn

def getActiveTargets():
    list = []
    try:
        conec  = conn.execute(TargetsModel.select().where(TargetsModel.c.active == True)).all()
        
        for publication in conec:
            list.append(publication._asdict())

    except ValueError:
        print(ValueError)
        print("ERROR: [src.services: targets] - Error ocurred in find active targets")
        list = []

    return list