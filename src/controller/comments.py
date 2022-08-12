# Libs
from datetime import datetime, timedelta

from src.libs.comments import get_comments_ofvideos, get_comments_onevideo
from src.services.comments import createComment, updateComment, getCommentById
from src.services.replies import createReplies, getRepliesById, updateReplies

def saveCommentsByVideos(videos):
    try:
        result = get_comments_ofvideos(videos)
        commentsFind = result[0]
        repliesFind = result[1]
        
        for comment in commentsFind:
            commentExist = getCommentById(comment['id'])
            if not commentExist:
                createComment(comment)
            else:
                updateComment(comment, comment['id'],)
        
        for replie in repliesFind:
            replieExist = getRepliesById(replie['id'])
            if not replieExist:
                createReplies(replie)
            else:
                updateReplies(replie, replie['id'],)
        
    except ValueError:
        print(ValueError)
        print("ERROR: [src.controller: comments saveCommentsByVideos] - Error ocurred in find and save comments videos")

def saveCommentsByVideo(video):
    try:
        result = get_comments_onevideo(video['id'], video['commentCount'])
        commentsFind = result[0]
        repliesFind = result[1]
        
        for comment in commentsFind:
            commentExist = getCommentById(comment['id'])
            if not commentExist:
                createComment(comment)
            else:
                updateComment(comment, comment['id'],)
        
        for replie in repliesFind:
            replieExist = getRepliesById(replie['id'])
            if not replieExist:
                createReplies(replie)
            else:
                updateReplies(replie, replie['id'],)
        
    except ValueError:
        print(ValueError)
        print("ERROR: [src.controller: comments saveCommentsByVideos] - Error ocurred in find and save comments of one video")