from .connection import youtube_authenticate
import urllib.parse as p
from datetime import datetime, timedelta
import re
import logging

# authenticate to YouTube API
youtube = youtube_authenticate()

def get_video_details(youtube, **kwargs):
    return youtube.videos().list(
        part="snippet,contentDetails,statistics",
        **kwargs
    ).execute()

def get_channel_videos(youtube, **kwargs):
    return youtube.search().list(
        **kwargs
    ).execute()

def get_video_search(youtube, **kwargs):
    return youtube.search().list(
        part="snippet",
        **kwargs
    ).execute()

def get_video_id_by_url(url):
    
    parsed_url = p.urlparse(url)
    
    video_id = p.parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        logging.error(f"Wasn't able to parse video URL: {url}")
        raise Exception(f"Wasn't able to parse video URL: {url}")

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
        
    tiempo = duration.split("PT")[1]

    hora = '00'
    minuto = '00'
    segundos = '00'

    if tiempo.__contains__('H'):
        hora = tiempo.split('H')[0]
        tiempo = tiempo.split('H')[1]
        if tiempo.__contains__('M'):
            minuto = tiempo.split('M')[0]
            tiempo = tiempo.split('M')[1]
            if tiempo.__contains__('S'):
                segundos =  tiempo.split('S')[0]
        elif tiempo.__contains__('S'):
            segundos =  tiempo.split('S')[0]
    elif tiempo.__contains__('M'):
        minuto = tiempo.split('M')[0]
        tiempo = tiempo.split('M')[1]
        if tiempo.__contains__('S'):
            segundos =  tiempo.split('S')[0]
    elif tiempo.__contains__('S'):
        segundos =  tiempo.split('S')[0]

    duration_str = hora+':'+minuto+':'+segundos
    
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
        'date_update': datetime.now()
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
        if 'tags' in snippet:
            for tag in snippet["tags"]:
                tags = tags + tag +' '
            
        duration = content_details["duration"]
        
        tiempo = duration.split("PT")[1]

        hora = '00'
        minuto = '00'
        segundos = '00'

        if tiempo.__contains__('H'):
            hora = tiempo.split('H')[0]
            tiempo = tiempo.split('H')[1]
            if tiempo.__contains__('M'):
                minuto = tiempo.split('M')[0]
                tiempo = tiempo.split('M')[1]
                if tiempo.__contains__('S'):
                    segundos =  tiempo.split('S')[0]
            elif tiempo.__contains__('S'):
                segundos =  tiempo.split('S')[0]
        elif tiempo.__contains__('M'):
            minuto = tiempo.split('M')[0]
            tiempo = tiempo.split('M')[1]
            if tiempo.__contains__('S'):
                segundos =  tiempo.split('S')[0]
        elif tiempo.__contains__('S'):
            segundos =  tiempo.split('S')[0]

        duration_str = hora+':'+minuto+':'+segundos

        if 'likeCount' in statistics:
            likes = statistics["likeCount"]
        else:
            likes = None
        
        if 'commentCount' in statistics:
            comments = statistics["commentCount"]
        else:
            comments = None

        video = {
            'id': videos_ids[count],
            'channelId': snippet["channelId"],
            'channelTitle': snippet["channelTitle"],
            'publishedAt': snippet["publishedAt"],
            'title': snippet["title"],
            'description': snippet["description"],
            'tags': tags,
            'viewCount': statistics["viewCount"],
            'likeCount': likes,
            'favoriteCount': statistics['favoriteCount'],
            'commentCount': comments,
            'duration': duration_str,
            'date_update': datetime.now()
        }

        videos.append(video)
        count += 1
        
    return videos

def get_videosSearch_info_byId(videos_ids, search):
    video_response = get_video_details(youtube, id=','.join(videos_ids[0:len(videos_ids)]))
    count = 0
    videos = []
    for video in video_response.get("items"):
        
        snippet         = video["snippet"]
        statistics      = video["statistics"]
        content_details = video["contentDetails"]
        
        logging.info(f'Extrayendo informacion del video '+ videos_ids[count])
            
        tags=''
        if 'tags' in snippet:
            for tag in snippet["tags"]:
                tags = tags + tag +' '
            
        duration = content_details["duration"]
        
        tiempo = duration.split("PT")[1]

        hora = '00'
        minuto = '00'
        segundos = '00'

        if tiempo.__contains__('H'):
            hora = tiempo.split('H')[0]
            tiempo = tiempo.split('H')[1]
            if tiempo.__contains__('M'):
                minuto = tiempo.split('M')[0]
                tiempo = tiempo.split('M')[1]
                if tiempo.__contains__('S'):
                    segundos =  tiempo.split('S')[0]
            elif tiempo.__contains__('S'):
                segundos =  tiempo.split('S')[0]
        elif tiempo.__contains__('M'):
            minuto = tiempo.split('M')[0]
            tiempo = tiempo.split('M')[1]
            if tiempo.__contains__('S'):
                segundos =  tiempo.split('S')[0]
        elif tiempo.__contains__('S'):
            segundos =  tiempo.split('S')[0]

        duration_str = hora+':'+minuto+':'+segundos

        if 'likeCount' in statistics:
            likes = statistics["likeCount"]
        else:
            likes = None
        
        if 'commentCount' in statistics:
            comments = statistics["commentCount"]
        else:
            comments = None

        video = {
            'id': videos_ids[count],
            'searchTopic': search,
            'channelId': snippet["channelId"],
            'channelTitle': snippet["channelTitle"],
            'publishedAt': snippet["publishedAt"],
            'title': snippet["title"],
            'description': snippet["description"],
            'tags': tags,
            'viewCount': statistics["viewCount"],
            'likeCount': likes,
            'favoriteCount': statistics['favoriteCount'],
            'commentCount': comments,
            'duration': duration_str,
            'date_update': datetime.now()
        }

        videos.append(video)
        count += 1
        
    return videos

def get_video_list_byChannel(channel_id):
    videos = []
    logging.info(f'Extrayendo informacion de los videos del canal '+ channel_id)
    
    SINCE = datetime.now() + timedelta(days= 1)
    UNTIL = SINCE - timedelta(days= 63)
    
    result = 50
    params = {
                'part': 'snippet',
                'q': '',
                'channelId': channel_id,
                'type': 'video',
                'maxResults': 50,
                'publishedAfter': str(datetime.date(UNTIL))+'T00:00:00Z'
        }

    while result > 0: 
        res = get_channel_videos(youtube, **params)
        channel_videos = res.get("items")
        ids = []
        for video in channel_videos:
            video_id = video["id"]["videoId"]
            ids.append(video_id)   
        
        if len(ids)>0:
            videos =  videos + get_videos_info_byId(ids)
        
        if "nextPageToken" in res:
            params["pageToken"] =  res["nextPageToken"]
            flag = False
        else:
            flag = True

        if len(channel_videos)<= 50 and flag:
            result = 0
            
    logging.info(f'Cantidad de videos encontrados '+ str(len(videos)))
    return videos

def get_videos_by_search(search: str): 
    videos = []
    cantidad = 100
    logging.info(f'Extrayendo informacion de los videos de la consulta '+ search)
    params = {
            'q': search, 
            'maxResults': 50,
            'type': 'video', 
            'order': 'viewCount'
    }
    while cantidad > 0:
        response = get_video_search(youtube, **params)
        search_videos = response.get("items")
        ids = []
        for video in search_videos:
            video_id = video["id"]["videoId"]
            ids.append(video_id)   
        
        if len(ids)>0:
            videos =  videos + get_videosSearch_info_byId(ids, search)
        
        cantidad = cantidad - len(search_videos)
        
        if cantidad < 50:
            params['maxResults'] = cantidad
        if "nextPageToken" in response:
            params["pageToken"] =  response["nextPageToken"]   
    logging.info(f'Cantidad de videos encontrados '+ str(len(videos)))
    return videos