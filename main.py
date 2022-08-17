from datetime import datetime

from src.controller.video import saveVideosByChannel, saveVideoByUrl, saveVideoBySearch
from src.controller.channel import saveChannel
from src.controller.comments import saveCommentsByVideo, saveCommentsByVideos
from src.controller.automatic import automaticChannel, automaticSearch

import typer

app = typer.Typer()

import logging

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

#Camando para extraer la informacion del canal, todos los videos de 2 meses y los comentarios de cada video, de la lista de targets activos. 
#Comando: python main.py automatic-channel
@app.command()
def automatic_channel():
    automaticChannel()

#Camando para extraer los primeros 100 videos y los comentarios de cada video, dado un topico de busqueda, por defecto estan oranizados por orden de cantidad de views. De la lista de topics activos. 
#Comando: python main.py automatic-search
@app.command()
def automatic_search():
    automaticSearch()

#Comando que se usa para extraer comentario de un video usando su url, ejemplo url: https://www.youtube.com/watch?v=1oeD2m2UQAI importante: la url debe tener el 'v=....'. 
#Comando: python main.py get-commnetsvideo https://www.youtube.com/watch?v=1oeD2m2UQAI
@app.command()
def get_commnetsVideo(url: str):
    print('Video '+ url)
    logging.info(f'Aqui empieza extraccion del video '+ url)
    video = saveVideoByUrl(url)
    saveCommentsByVideo(video)

#Comando para encontrar y guardar un video usando su url, ejemplo url: https://www.youtube.com/watch?v=1oeD2m2UQAI importante: la url debe tener el 'v=....'
#Comando: python main.py get-video https://www.youtube.com/watch?v=1oeD2m2UQAI
@app.command()
def get_video(url: str):
    print('Video '+ url)
    logging.info(f'Aqui empieza extraccion del video '+ url)
    saveVideoByUrl(url)

#Camando para extraer la informacion del canal, todos los videos de 2 meses y los comentarios de cada video, dado el nombre de un canal. 
#Comando: python main.py get-all-bychannel telemundo
@app.command()
def get_all_bychannel(channel: str):
    print('Channel '+channel)
    logging.info(f'Aqui empieza extraccion del canal '+ channel)
    saveChannel(channel)
    logging.info(f'Aqui empieza extraccion de los videos del canal '+ channel)
    videos = saveVideosByChannel(channel)
    logging.info(f'Aqui empieza la extraccion de los comentarios de los videos del canal '+ channel)
    saveCommentsByVideos(videos)

#Comando para extraer la informacion de un canal, dado el nombre del mismo
#Comando: python main.py get-channel telemundo
@app.command()
def get_channel(channel: str):
    print('Channel '+channel)
    logging.info(f'Aqui empieza extraccion del canal '+ channel)
    saveChannel(channel)

#Camando para extraer los primeros 100 videos y los comentarios de cada video, dado un topico de busqueda, por defecto estan oranizados por orden de cantidad de views. 
#Comando: python main.py get-search viajar  
@app.command()
def get_search(search: str):
    print('search '+ search)
    logging.info(f'Aqui empieza extraccion de videos por busqueda '+ search)
    videos = saveVideoBySearch(search)
    logging.info(f'Aqui empieza la extraccion de los comentarios de los videos de la busqueda '+ search)
    saveCommentsByVideos(videos)

#Camando para extraer todos los videos de 2 meses, dado el nombre de un canal. 
#Comando: python main.py get-channelvideos telemundo
@app.command()
def get_channelvideos(channel: str):
    print('channel videos')
    logging.info(f'Aqui empieza extraccion de los videos del canal '+ channel)
    saveVideosByChannel(channel)

#Camando para extraer todos los videos de 2 meses y los comentarios de cada video, dado el nombre de un canal. 
#Comando: python main.py get-channelvideosandcomments telemundo
@app.command()
def get_channelvideosandcomments(channel: str):
    print('channel videos')
    logging.info(f'Aqui empieza extraccion de los videos del canal '+ channel)
    videos = saveVideosByChannel(channel)
    logging.info(f'Aqui empieza la extraccion de los comentarios de los videos del canal '+ channel)
    saveCommentsByVideos(videos)

if __name__ == "__main__":
    app()