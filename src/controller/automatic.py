# Libs
from datetime import datetime, timedelta

#services
from src.services.targets import getActiveTargets
from src.services.topics import getActiveTopics

#controllers
from src.controller.channel import saveChannel
from src.controller.comments import saveCommentsByVideos
from src.controller.video import saveVideoBySearch, saveVideosByChannel

import logging

def automaticChannel():
    targets = getActiveTargets()
    for target in targets:
        logging.info(f'Aqui empieza extraccion del canal '+ target['channelName'])
        saveChannel(target['channelName'])
        logging.info(f'Aqui empieza extraccion de los videos del canal '+ target['channelName'])
        videos = saveVideosByChannel(target['channelName'])
        logging.info(f'Aqui empieza la extraccion de los comentarios de los videos del canal '+ target['channelName'])
        saveCommentsByVideos(videos)

def automaticSearch():
    topics = getActiveTopics()
    for topic in topics:
        logging.info(f'Aqui empieza extraccion de videos por busqueda '+ topic['topic'])
        videos = saveVideoBySearch(topic['topic'])
        logging.info(f'Aqui empieza la extraccion de los comentarios de los videos de la busqueda '+ topic['topic'])
        saveCommentsByVideos(videos)

