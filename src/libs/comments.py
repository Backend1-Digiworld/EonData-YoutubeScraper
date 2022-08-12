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
    logging.info(f'Extrayendo informacion de los comentarios de '+str(len(videos))+' los videos')
    for video in videos:
        logging.info(f'Extrayendo informacion de los comentarios del video '+video['id'] +' total comentarios: '+str(video['commentCount']))
        cantidad = video['commentCount']
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
                comment = {
                    'id': item["snippet"]["topLevelComment"]["id"],
                    'videoId': video['id'],
                    'textDisplay': item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                    'textOriginal': item["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                    'authorDisplayName': item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                    'authorProfileImageUrl': item["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"],
                    'authorChannelUrl': item["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"],
                    'authorChannelId': item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]['value'],
                    'likeCount': item["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                    'totalReplyCount': item["snippet"]["totalReplyCount"],
                    'publishedAt': item["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                    'updatedAt': item["snippet"]["topLevelComment"]["snippet"]["updatedAt"],
                    'date_update': datetime.now()
                }
                comments.append(comment)
                
                if 'replies' in item:
                    comment_replies = item['replies']['comments']
                    for replie in comment_replies:
                        rep = {
                            'id': replie['id'],
                            'commentId': item["snippet"]["topLevelComment"]["id"],
                            'videoId': video['id'],
                            'textDisplay': replie["snippet"]["textDisplay"],
                            'textOriginal': replie["snippet"]['textOriginal'],
                            'authorDisplayName': replie["snippet"]["authorDisplayName"],
                            'authorProfileImageUrl': replie["snippet"]["authorProfileImageUrl"],
                            'authorChannelUrl': replie["snippet"]["authorChannelUrl"],
                            'authorChannelId': replie["snippet"]["authorChannelId"]['value'],
                            'likeCount': replie["snippet"]["likeCount"],
                            'publishedAt': replie["snippet"]["publishedAt"],
                            'updatedAt': replie["snippet"]["updatedAt"],
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
            comment = {
                'id': item["snippet"]["topLevelComment"]["id"],
                'videoId': videoId,
                'textDisplay': item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                'textOriginal': item["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                'authorDisplayName': item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                'authorProfileImageUrl': item["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"],
                'authorChannelUrl': item["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"],
                'authorChannelId': item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]['value'],
                'likeCount': item["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                'totalReplyCount': item["snippet"]["totalReplyCount"],
                'publishedAt': item["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                'updatedAt': item["snippet"]["topLevelComment"]["snippet"]["updatedAt"],
                'date_update': datetime.now()
            }
            comments.append(comment)
                
            if 'replies' in item:
                comment_replies = item['replies']['comments']
                for replie in comment_replies:
                    rep = {
                        'id': replie['id'],
                        'commentId': item["snippet"]["topLevelComment"]["id"],
                        'videoId': videoId,
                        'textDisplay': replie["snippet"]["textDisplay"],
                        'textOriginal': replie["snippet"]['textOriginal'],
                        'authorDisplayName': replie["snippet"]["authorDisplayName"],
                        'authorProfileImageUrl': replie["snippet"]["authorProfileImageUrl"],
                        'authorChannelUrl': replie["snippet"]["authorChannelUrl"],
                        'authorChannelId': replie["snippet"]["authorChannelId"]['value'],
                        'likeCount': replie["snippet"]["likeCount"],
                        'publishedAt': replie["snippet"]["publishedAt"],
                        'updatedAt': replie["snippet"]["updatedAt"],
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