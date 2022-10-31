from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ as env
from sqlalchemy.ext.declarative import declarative_base
import config

config.load()
engine = create_engine(env.get("DB_STRING"), pool_size=4, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()
