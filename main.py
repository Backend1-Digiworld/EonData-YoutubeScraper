from datetime import datetime

from src.libs.video import get_video_id_by_url, get_video_info, get_vide_list_byChannel
from src.libs.channel import get_channel_info

import typer

app = typer.Typer()

import logging

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

@app.command()
def get_video(url: str):
    print('Video '+ url)
    logging.info(f'Aqui empieza extraccion del video '+ url)
    video_id = get_video_id_by_url(url)
    get_video_info(video_id)

@app.command()
def get_channel(channel: str):
    print('Channel '+channel)
    logging.info(f'Aqui empieza extraccion del canal '+ channel)
    get_channel_info(channel)
    
    
@app.command()
def get_search(search: str):
    print('search')

@app.command()
def get_channelvideos(channel: str):
    print('channel videos')
    logging.info(f'Aqui empieza extraccion del los videos del canal '+ channel)
    get_vide_list_byChannel(channel)

@app.command()
def get_channelandvideos(channel: str):
    print('Channel '+channel)
    logging.info(f'Aqui empieza extraccion del canal '+ channel)
    get_channel_info(channel)
    logging.info(f'Aqui empieza extraccion del los videos del canal '+ channel)
    get_vide_list_byChannel(channel)

if __name__ == "__main__":
    app()