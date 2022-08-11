from .connection import youtube_authenticate
import urllib.parse as p
from datetime import datetime, timedelta
import re
import logging

# authenticate to YouTube API
youtube = youtube_authenticate()

def get_video_id_by_url(url):
    
    parsed_url = p.urlparse(url)
    
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        logging.error(f"Wasn't able to parse video URL: {url}")
        raise Exception(f"Wasn't able to parse video URL: {url}")

def get_video_details(youtube, **kwargs):
    return youtube.videos().list(
        part="snippet,contentDetails,statistics",
        **kwargs
    ).execute()

def get_channel_videos(youtube, **kwargs):
    return youtube.search().list(
        **kwargs
    ).execute()

def get_video_info(video_id):
    video_response = get_video_details(youtube, id=video_id)
    items = video_response.get("items")[0]
    
    snippet         = items["snippet"]
    statistics      = items["statistics"]
    content_details = items["contentDetails"]
    logging.info(f'Extrayendoinformacion del video '+ video_id)
    tags=''
    for tag in snippet["tags"]:
        tags = tags + tag +' '
    
    duration = content_details["duration"]
    
    parsed_duration = re.search(f"PT(\d+H)?(\d+M)?(\d+S)", duration).groups()
    duration_str = ""
    for d in parsed_duration:
        if d:
            duration_str += f"{d[:-1]}:"
    duration_str = duration_str.strip(":")
    
    video = {
        'id': video_id,
        'channelId': snippet["channelId"],
        'channelTitle': snippet["channelTitle"],
        'publishedAt': snippet["publishedAt"],
        'title': snippet["title"],
        'description': snippet["description"],
        'video_pic': snippet["thumbnails"]["high"]["url"],
        'tags': tags,
        'viewCount': statistics["viewCount"],
        'likeCount': statistics["likeCount"],
        'favoriteCount': statistics['favoriteCount'],
        'commentCount': statistics["commentCount"],
        'duration': duration_str,
        'date_update': datetime.utcnow()
    }
    
    return video

def get_videos_info_byId(videos_ids):
    video_response = get_video_details(youtube, id=','.join(videos_ids[0:len(videos_ids)]))
    count = 0
    videos = []
    for video in video_response.get("items"):
        
        snippet         = video["snippet"]
        statistics      = video["statistics"]
        content_details = video["contentDetails"]
        
        logging.info(f'Extrayendo informacion del video '+ videos_ids[count])
            
        tags=''
        for tag in snippet["tags"]:
            tags = tags + tag +' '
            
        duration = content_details["duration"]
        
        if re.search(f"PT(\d+H)?(\d+M)?(\d+S)", duration) == None:
            if re.search(f"PT(\d+H)?(\d+M)", duration) == None:
                parsed_duration = re.search(f"PT(\d+H)", duration).groups()   
            else: 
                parsed_duration = re.search(f"PT(\d+H)?(\d+M)", duration).groups()   
        else: 
            parsed_duration = re.search(f"PT(\d+H)?(\d+M)?(\d+S)", duration).groups()
        duration_str = ""
        for d in parsed_duration:
            if d:
                duration_str += f"{d[:-1]}:"
        duration_str = duration_str.strip(":")
            
        video = {
            'id': videos_ids[count],
            'channelId': snippet["channelId"],
            'channelTitle': snippet["channelTitle"],
            'publishedAt': snippet["publishedAt"],
            'title': snippet["title"],
            'description': snippet["description"],
            'tags': tags,
            'viewCount': statistics["viewCount"],
            'likeCount': statistics["likeCount"],
            'favoriteCount': statistics['favoriteCount'],
            'commentCount': statistics["commentCount"],
            'duration': duration_str,
            'date_update': datetime.utcnow()
        }

        videos.append(video)
        count += 1
        
    return videos

def get_vide_list_byChannel(channel_id):
    videos = []
    logging.info(f'Extrayendo informacion de los videos del canal '+ channel_id)
    
    SINCE = datetime.now() + timedelta(days= 1)
    UNTIL = SINCE - timedelta(days= 60)
    
    while SINCE >= UNTIL:
        params = {
                'part': 'snippet',
                'q': '',
                'channelId': channel_id,
                'type': 'video',
                'maxResults': 100,
                'order': 'date',
                'publishedBefore': str(datetime.date(SINCE))+'T00:00:00Z'
        }
            
        res = get_channel_videos(youtube, **params)
        channel_videos = res.get("items")
        ids = []
        for video in channel_videos:
            video_id = video["id"]["videoId"]
            date = datetime.strptime(video['snippet']["publishedAt"].split("T")[0], '%Y-%m-%d')
            if date >= UNTIL:
                ids.append(video_id)   
        
        if len(ids)>0:
            videos =  videos + get_videos_info_byId(ids)
        
        fecha = res.get("items")[len(res.get("items"))-1]['snippet']["publishedAt"].split("T")[0]
        SINCE = datetime.strptime(fecha, '%Y-%m-%d')
            
    logging.info(f'Cantidad de videos encontrados '+ str(len(videos)))
    return videos