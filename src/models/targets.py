from datetime import datetime
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, DateTime, Text
from src.settings.database import meta, engine

TargetsModel = Table(
    "targets", meta, 
    Column("id", Integer, primary_key=True),
    Column('channelName', String(500)),
    Column('active', Boolean),
)

meta.create_all(engine)