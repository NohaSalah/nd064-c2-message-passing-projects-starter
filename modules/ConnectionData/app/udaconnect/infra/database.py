# like config file
import os
from typing import List, Type
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

SQLALCHEMY_DATABASE_URI = ( f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"   )

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
