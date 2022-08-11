from datetime import datetime
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime, Text
from src.settings.database import meta, engine

VideoModel = Table(
    "channel", meta, 
    Column("id", String(255), primary_key=True),
    Column("title", Text),
    Column("description", Text),
    Column("publishedAt", DateTime),
    Column("channel_pic", Text),
    Column("country", String(500)),
    Column("viewCount", Integer),
    Column("subscriberCount", Integer),
    Column("videoCount", Integer),
    Column("date_update", DateTime, default=datetime.utcnow())
)

meta.create_all(engine)