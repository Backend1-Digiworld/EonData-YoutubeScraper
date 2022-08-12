from xxlimited import Null
from .connection import youtube_authenticate
import urllib.parse as p
from datetime import date, datetime
import logging

# authenticate to YouTube API
youtube = youtube_authenticate()

def get_channel_details(youtube, **kwargs):
    return youtube.channels().list(
        part="statistics,snippet,contentDetails",
        **kwargs
    ).execute()

def search(youtube, **kwargs):
    return youtube.search().list(
        part="snippet",
        **kwargs
    ).execute()

def get_channelId(channel: str):
    response = search(youtube, q=channel, maxResults=1, type='channel',)
    items = response.get("items")
    if items:
        channel_id = items[0]["snippet"]["channelId"]
        return channel_id

def get_channel_info(channel_id):
    response = get_channel_details(youtube, id=channel_id)
    
    snippet = response["items"][0]["snippet"]
    statistics = response["items"][0]["statistics"]
    logging.info(f'Extrayendo informacion de los videos del canal '+ channel_id)
    
    if 'country' in snippet:
        country = snippet['country']
    else:
        country = None

    channel = {
        'id': channel_id,
        'title': snippet['title'],
        'description': snippet['description'],
        'publishedAt': snippet['publishedAt'],
        'channel_pic': snippet["thumbnails"]["high"]["url"],
        'country': country,
        'viewCount': statistics['viewCount'],
        'subscriberCount': statistics['subscriberCount'],
        'videoCount': statistics['videoCount'],
        'date_update': datetime.now()
    }
    
    return channel