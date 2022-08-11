from googleapiclient.discovery import build

def youtube_authenticate():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = 'AIzaSyBzAyvF34ih8qenJdvoCi42piU6mIsBTYM'

    return build(api_service_name, api_version, developerKey=api_key)
