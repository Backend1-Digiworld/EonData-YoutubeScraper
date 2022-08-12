# Libs
from datetime import datetime, timedelta

from requests import get

from src.libs.channel import get_channel_info, get_channelId
from src.services.channel import createChannel, getChannelById, getChannelByName, updateChannel

def saveChannel(channelName: str):
    channel = {}
    try:
        channelId = get_channelId(channelName)
        channel = get_channel_info(channelId)
        
        channelExist = getChannelById(channelId)
        if not channelExist:
            createChannel(channel)
        else:    
            updateChannel(channel, str(channel['id']))  
    except ValueError:
        print(ValueError)
        print("ERROR: [controller: channel saveChannel] - Error ocurred in find and save channel")
    return channel