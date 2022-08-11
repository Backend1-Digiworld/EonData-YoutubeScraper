from .connection import youtube_authenticate
import urllib.parse as p
from datetime import datetime
import logging

# authenticate to YouTube API
youtube = youtube_authenticate()

def get_channel_details(youtube, **kwargs):
    return youtube.channels().list(
        part="statistics,snippet,contentDetails",
        **kwargs
    ).execute()

def get_channel_info(channel_id):
    response = get_channel_details(youtube, id=channel_id)
    
    snippet = response["items"][0]["snippet"]
    statistics = response["items"][0]["statistics"]
    logging.info(f'Extrayendo informacion de los videos del canal '+ channel_id)
    channel = {
        'id': channel_id,
        'title': snippet['title'],
        'description': snippet['description'],
        'publishedAt': snippet['publishedAt'],
        'channel_pic': snippet["thumbnails"]["high"]["url"],
        'country': snippet['country'],
        'viewCount': statistics['viewCount'],
        'subscriberCount': statistics['subscriberCount'],
        'videoCount': statistics['videoCount']
    }
    
    return channel