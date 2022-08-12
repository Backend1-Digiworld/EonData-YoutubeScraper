from datetime import datetime

from src.controller.video import saveVideosByChannel, saveVideoByUrl, saveVideoBySearch
from src.controller.channel import saveChannel
from src.controller.comments import saveCommentsByVideo, saveCommentsByVideos

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
def get_commnetsVideo(url: str):
    print('Video '+ url)
    logging.info(f'Aqui empieza extraccion del video '+ url)
    video = saveVideoByUrl(url)
    saveCommentsByVideo(video)

@app.command()
def get_video(url: str):
    print('Video '+ url)
    logging.info(f'Aqui empieza extraccion del video '+ url)
    saveVideoByUrl(url)
    
@app.command()
def get_all_bychannel(channel: str):
    print('Channel '+channel)
    logging.info(f'Aqui empieza extraccion del canal '+ channel)
    saveChannel(channel)
    logging.info(f'Aqui empieza extraccion de los videos del canal '+ channel)
    videos = saveVideosByChannel(channel)
    logging.info(f'Aqui empieza la extraccion de los comentarios de los videos del canal '+ channel)
    saveCommentsByVideos(videos)
    
@app.command()
def get_channel(channel: str):
    print('Channel '+channel)
    logging.info(f'Aqui empieza extraccion del canal '+ channel)
    saveChannel(channel)
    
@app.command()
def get_search(search: str):
    print('search '+ search)
    logging.info(f'Aqui empieza extraccion de videos por busqueda '+ search)
    videos = saveVideoBySearch(search)
    logging.info(f'Aqui empieza la extraccion de los comentarios de los videos de la busqueda '+ search)
    saveCommentsByVideos(videos)

@app.command()
def get_channelvideos(channel: str):
    print('channel videos')
    logging.info(f'Aqui empieza extraccion de los videos del canal '+ channel)
    saveVideosByChannel(channel)

@app.command()
def get_channelvideosandcomments(channel: str):
    print('channel videos')
    logging.info(f'Aqui empieza extraccion de los videos del canal '+ channel)
    videos = saveVideosByChannel(channel)
    logging.info(f'Aqui empieza la extraccion de los comentarios de los videos del canal '+ channel)
    saveCommentsByVideos(videos)

@app.command()
def get_channelandvideos(channel: str):
    print('Channel '+channel)
    logging.info(f'Aqui empieza extraccion del canal '+ channel)
    saveChannel(channel)
    logging.info(f'Aqui empieza extraccion de los videos del canal '+ channel)
    saveVideosByChannel(channel)

if __name__ == "__main__":
    app()