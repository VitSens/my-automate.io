from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql://localhost:5432/postgres?user=postgres&password=postgres')
base = declarative_base()

Session = sessionmaker(engine)
session = Session()

base.metadata.create_all(engine)
