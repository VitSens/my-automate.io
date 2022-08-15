import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = os.getenv('POSTGRES_URI')

db = create_engine(db_string)
base = declarative_base()

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)
