from datetime import datetime
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime, Text
from src.settings.database import meta, engine

VideoModel = Table(
    "video", meta, 
    Column("id", String(255), primary_key=True),
    Column("channelId", String(500)),
    Column("channelTitle", String(500)),
    Column("publishedAt", DateTime),
    Column("title", Text),
    Column("description", Text),
    Column("video_pic", Text),
    Column("tags", Text),
    Column("viewCount", Integer),
    Column("likeCount", Integer),
    Column("favoriteCount", Integer),
    Column("commentCount", Integer),
    Column("duration", String(500)),
    Column("date_update", DateTime, default=datetime.utcnow())
)

meta.create_all(engine)