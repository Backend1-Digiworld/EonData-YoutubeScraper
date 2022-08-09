# Libs
from sqlalchemy import create_engine, MetaData

# ENv variables
from .settings import DB_ENGINE, DB_DRIV, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

# Defined connection string
connectionString =  DB_ENGINE + "+" + DB_DRIV + "://" + DB_USER +":" + DB_PASS + "@" + DB_HOST + ":" + DB_PORT + "/" + DB_NAME;
engine = create_engine(connectionString)

# Create connection
meta = MetaData()
conn = engine.connect()
