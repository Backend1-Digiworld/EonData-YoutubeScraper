from .connection import youtube_authenticate
import urllib.parse as p
from datetime import datetime, timedelta
import re
import logging

# authenticate to YouTube API
youtube = youtube_authenticate()

def get_comments(youtube, **kwargs):
    return youtube.commentThreads().list(
        part="snippet,replies",
        **kwargs
    ).execute()

def get_comments_ofvideos(videos):
    comments = []
    replies = []
    logging.info(f'Extrayendo informacion de los comentarios de '+str(len(videos))+' videos')
    for video in videos:
        logging.info(f'Extrayendo informacion de los comentarios del video '+video['id'] +' total comentarios: '+str(video['commentCount']))
        
        if video['commentCount'] != None:
            cantidad = int(video['commentCount'])
        else:
            cantidad = 0
        
        if cantidad < 100:
            result = cantidad
        else:
            result = 100
        params = {
            'videoId': video['id'], 
            'maxResults': result,
        }
        cantidadEncontrados = 0
        while cantidad > 0:
            totalreplies = 0
            response = get_comments(youtube, **params)
            items = response.get("items")
            if not items:
                break
            for item in items:
                if 'authorChannelId' in item["snippet"]["topLevelComment"]["snippet"]:
                    autor = item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]['value']
                else:
                    autor = None

                if item["snippet"]["topLevelComment"]["snippet"]["publishedAt"].__contains__('.'):
                    fecha = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"].split(".")[0]
                    publishedAt = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S')
                else:
                    publishedAt = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                
                if item["snippet"]["topLevelComment"]["snippet"]["updatedAt"].__contains__('.'):
                    fecha = item["snippet"]["topLevelComment"]["snippet"]["updatedAt"].split(".")[0]
                    updatedAt = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S')
                else:
                    updatedAt = item["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
                
                comment = {
                    'id': item["snippet"]["topLevelComment"]["id"],
                    'videoId': video['id'],
                    'textDisplay': item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                    'textOriginal': item["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                    'authorDisplayName': item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                    'authorProfileImageUrl': item["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"],
                    'authorChannelUrl': item["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"],
                    'authorChannelId': autor,
                    'likeCount': item["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                    'totalReplyCount': item["snippet"]["totalReplyCount"],
                    'publishedAt': publishedAt,
                    'updatedAt': updatedAt,
                    'date_update': datetime.now()
                }
                comments.append(comment)
                
                if 'replies' in item:
                    comment_replies = item['replies']['comments']
                    for replie in comment_replies:
                        if 'authorChannelId' in replie["snippet"]:
                            autorrep = replie["snippet"]["authorChannelId"]['value']
                        else:
                            autorrep = None
                        
                        if 'totalReplyCount' in replie["snippet"]:
                            replycount = replie["snippet"]
                        else:
                            replycount = 0
                        
                        if replie["snippet"]["publishedAt"].__contains__('.'):
                            fecha = replie["snippet"]["publishedAt"].split(".")[0]
                            publishedAt = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S')
                        else: 
                            publishedAt = replie["snippet"]["publishedAt"]
                        
                        if replie["snippet"]["updatedAt"].__contains__('.'):
                            fecha = replie["snippet"]["updatedAt"].split(".")[0]
                            updatedAt = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S')
                        else:
                            updatedAt = replie["snippet"]["updatedAt"]
                        
                        rep = {
                            'id': replie['id'],
                            'commentId': item["snippet"]["topLevelComment"]["id"],
                            'videoId': video['id'],
                            'textDisplay': replie["snippet"]["textDisplay"],
                            'textOriginal': replie["snippet"]['textOriginal'],
                            'authorDisplayName': replie["snippet"]["authorDisplayName"],
                            'authorProfileImageUrl': replie["snippet"]["authorProfileImageUrl"],
                            'authorChannelUrl': replie["snippet"]["authorChannelUrl"],
                            'authorChannelId': autorrep,
                            'likeCount': replie["snippet"]["likeCount"],
                            'totalReplyCount': replycount,
                            'publishedAt': publishedAt,
                            'updatedAt': updatedAt,
                            'date_update': datetime.now()
                        }
                        replies.append(rep)
                totalreplies += item["snippet"]["totalReplyCount"] 
            
            if "nextPageToken" in response:
                params["pageToken"] =  response["nextPageToken"]
                
            cantidad = cantidad-len(items)-totalreplies
            
            if cantidad < 100:
                params["maxResults"] = cantidad

            cantidadEncontrados +=len(items)+totalreplies
        logging.info(f'Total comentarios: '+str(cantidadEncontrados)+' del video '+video['id'])
    
    logging.info(f'Cantidad de comentarios encontrados '+ str(len(comments)+len(replies)))
    return [comments, replies]

def get_comments_onevideo(videoId, videoCommnets):
    comments = []
    replies = []
    logging.info(f'Extrayendo informacion de los comentarios del video '+videoId +' total comentarios: '+str(videoCommnets))
    cantidad = videoCommnets
    if cantidad < 100:
        result = cantidad
    else:
        result = 100
    params = {
        'videoId': videoId, 
        'maxResults': result,
    }
    cantidadEncontrados = 0
    while cantidad > 0:
        totalreplies = 0
        response = get_comments(youtube, **params)
        items = response.get("items")
        if not items:
            break
        for item in items:
            if 'authorChannelId' in item["snippet"]["topLevelComment"]["snippet"]:
                autor = item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]['value']
            else:
                autor = None
                
            if item["snippet"]["topLevelComment"]["snippet"]["publishedAt"].__contains__('.'):
                fecha = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"].split(".")[0]
                publishedAt = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S')
            else:
                publishedAt = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
            
            if item["snippet"]["topLevelComment"]["snippet"]["updatedAt"].__contains__('.'):
                fecha = item["snippet"]["topLevelComment"]["snippet"]["updatedAt"].split(".")[0]
                updatedAt = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S')
            else:
                updatedAt = item["snippet"]["topLevelComment"]["snippet"]["updatedAt"]
            
            comment = {
                'id': item["snippet"]["topLevelComment"]["id"],
                'videoId': videoId,
                'textDisplay': item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                'textOriginal': item["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                'authorDisplayName': item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                'authorProfileImageUrl': item["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"],
                'authorChannelUrl': item["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"],
                'authorChannelId': autor,
                'likeCount': item["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                'totalReplyCount': item["snippet"]["totalReplyCount"],
                'publishedAt': publishedAt,
                'updatedAt': updatedAt,
                'date_update': datetime.now()
            }
            comments.append(comment)
                
            if 'replies' in item:
                comment_replies = item['replies']['comments']
                for replie in comment_replies:
                    if 'authorChannelId' in replie["snippet"]:
                        autorrep = replie["snippet"]["authorChannelId"]['value']
                    else:
                        autorrep = None
                        
                    if 'totalReplyCount' in replie["snippet"]:
                        replycount = replie["snippet"]
                    else:
                        replycount = 0
                    
                    if replie["snippet"]["publishedAt"].__contains__('.'):
                        fecha = replie["snippet"]["publishedAt"].split(".")[0]
                        publishedAt = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S')
                    else: 
                        publishedAt = replie["snippet"]["publishedAt"]
                        
                    if replie["snippet"]["updatedAt"].__contains__('.'):
                        fecha = replie["snippet"]["updatedAt"].split(".")[0]
                        updatedAt = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S')
                    else:
                        updatedAt = replie["snippet"]["updatedAt"]
                    rep = {
                        'id': replie['id'],
                        'commentId': item["snippet"]["topLevelComment"]["id"],
                        'videoId': videoId,
                        'textDisplay': replie["snippet"]["textDisplay"],
                        'textOriginal': replie["snippet"]['textOriginal'],
                        'authorDisplayName': replie["snippet"]["authorDisplayName"],
                        'authorProfileImageUrl': replie["snippet"]["authorProfileImageUrl"],
                        'authorChannelUrl': replie["snippet"]["authorChannelUrl"],
                        'authorChannelId': autorrep,
                        'likeCount': replie["snippet"]["likeCount"],
                        'totalReplyCount': replycount,
                        'publishedAt': publishedAt,
                        'updatedAt': updatedAt,
                        'date_update': datetime.now()
                    }
                    replies.append(rep)
            totalreplies += item["snippet"]["totalReplyCount"] 
            
        if "nextPageToken" in response:
            params["pageToken"] =  response["nextPageToken"]
                
        cantidad = cantidad-len(items)-totalreplies
            
        if cantidad < 100:
            params["maxResults"] = cantidad

        cantidadEncontrados +=len(items)+totalreplies
    
    logging.info(f'Cantidad de comentarios encontrados '+ str(len(comments)+len(replies)))
    return [comments, replies]