from sqlalchemy import create_engine, Index
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:////mnt/c/Users/ehennenfent/wikidata/wikidata2.db")


from .models import Item, Property, RankData

Base.metadata.create_all(engine)
#
# sitelink_index = Index('item_sitelink_idx', Item.sitelink)
# view_index = Index('view_sitelink_idx', RankData.sitelink)
#
# sitelink_index.create(bind=engine)
# view_index.create(bind=engine)

Session = sessionmaker(bind=engine, expire_on_commit=False)
