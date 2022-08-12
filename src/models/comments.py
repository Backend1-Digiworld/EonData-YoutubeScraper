from datetime import datetime
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime, Text
from src.settings.database import meta, engine

CommentModel = Table(
    "comments", meta, 
    Column("id", String(500), primary_key=True),
    Column('videoId', String(500)),
    Column('textDisplay', Text),
    Column('textOriginal', Text),
    Column('authorDisplayName', Text),
    Column('authorProfileImageUrl', Text),
    Column('authorChannelUrl', Text),
    Column('authorChannelId', Text),
    Column('likeCount', Integer),
    Column('totalReplyCount', Integer),
    Column("publishedAt", DateTime),                
    Column('updatedAt', DateTime),                                
    Column("date_update", DateTime, default=datetime.utcnow())
)
                           
meta.create_all(engine)