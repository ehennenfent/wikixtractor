from sqlalchemy import create_engine, Index
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:////mnt/c/Users/ehennenfent/wikidata/wikidata.db")


from .models import Item, Property

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine, expire_on_commit=False)
