# Libs
from datetime import datetime, timedelta

from src.libs.channel import get_channel_info
from src.services.channel import createChannel, getChannelById, getChannelByName, updateChannel

def saveChannel(channel: str):
    channel = {}
    try:
        channel = get_channel_info(channel)
        
        channelExist = getChannelByName(channel)
        if not channelExist:
            createChannel(channel)
        else:    
            updateChannel(channel, str(channel['id']))  
    except ValueError:
        print(ValueError)
        print("ERROR: [controller: channel saveChannel] - Error ocurred in find and save channel")
    return channel