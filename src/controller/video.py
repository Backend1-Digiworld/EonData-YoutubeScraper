# Libs
from datetime import datetime, timedelta

from src.libs.video import get_video_id_by_url, get_video_info, get_video_list_byChannel, get_videos_by_search
from src.services.video import createVideo, getVideosById, getVideoByChannelName, getVideosByChannel, getVideosDays, updateVideo
from src.services.videosSearch import createVideoSearch, updateVideoSearch, getVideosSearchById, getVideosSearchByChannel
from src.libs.channel import get_channelId

import logging

def saveVideosByChannel(channel: str):
    try:
        videoComment = []
        date = datetime.now() - timedelta(days= 5)
        channelId = get_channelId(channel)
        videosFind = get_video_list_byChannel(channelId) 
        
        for video in videosFind:
            videoExist = getVideosById(video['id'])
            if not videoExist:
                logging.info(f'Guardando video '+ video['id']+' en base de datos')
                createVideo(video)
                videoComment.append(video)
            else:
                logging.info(f'Actualizando video '+ video['id']+' en base de datos')
                if video['date_update'] >= date:
                    if video['commentCount'] != videoExist['commentCount']:
                        videoComment.append(video) 
                updateVideo(video, video['id'],)
        return videoComment
    except ValueError:
        print(ValueError)
        print("ERROR: [src.controller: video saveVideosByChannel] - Error ocurred in find and save channel videos")
        return []
    
def saveVideoByUrl(url: str):
    try:
        video_id = get_video_id_by_url(url)
        video = get_video_info(video_id)
        videoExist = getVideosById(video_id)
        if not videoExist:
            logging.info(f'Guardando video '+ video['id']+' en base de datos')
            createVideo(video)
        else:
            logging.info(f'Actualizando video '+ video['id']+' en base de datos')
            updateVideo(video, video['id'],)
        return video
    except ValueError:
        print(ValueError)
        print("ERROR: [src.controller: video saveVideosByChannel] - Error ocurred in find and save channel videos")
        return {}
    
def saveVideoBySearch(search: str):
    try:
        videoComment = []
        date = datetime.now() - timedelta(days= 5)
        videosFind = get_videos_by_search(search) 
        for video in videosFind:
            videoExist = getVideosSearchById(video['id'])
            if not videoExist:
                logging.info(f'Guardando video '+ video['id']+' en base de datos')
                createVideoSearch(video)
                videoComment.append(video)
            else:
                logging.info(f'Actualizando video '+ video['id']+' en base de datos')
                if video['date_update'] >= date:
                    if video['commentCount'] != videoExist['commentCount']:
                        videoComment.append(video) 
                updateVideoSearch(video, video['id'],)
        return videoComment
    except ValueError:
        print(ValueError)
        print("ERROR: [src.controller: video saveVideosByChannel] - Error ocurred in find and save channel videos")

def getVideosOfChannel(channel):
    videos = []
    try:
        videos = getVideosByChannel(channel)
    except ValueError:
        print(ValueError)
        print("ERROR: [src.controller: video getVideosOfChannel] - Error ocurred in find videos by channel")
        videos = []
    return videos

def getvideoDays(days):
    videos = []
    try:
        videos = getvideoDays(days)
    except ValueError:
        print(ValueError)
        print("ERROR: [src.controller: video getvideoDays] - Error ocurred in find videos by days")
        videos = []
    return videos