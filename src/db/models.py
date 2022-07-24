from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON

from . import Base
import orjson as json

instance_table = Table(
    "instance_of",
    Base.metadata,
    Column("of", ForeignKey("items.id"), primary_key=True, autoincrement=False),
    Column(
        "is_instance", ForeignKey("items.id"), primary_key=True, autoincrement=False
    ),
)


class InstanceRecord(Base):
    __table__ = instance_table


class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    description = Column(String)
    claims = Column(JSON)

    @classmethod
    def from_visitor(cls, visitor):
        return cls(
            id=visitor.id,
            name=visitor.label,
            description=visitor.description,
            claims=visitor.claims,
        )


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    description = Column(String)
    sitelink = Column(String, index=True)
    views = Column(Integer, default=0)
    pagerank = Column(Float, default=0.0)
    claims = Column(JSON)
    instance_of = relationship(
        "Item",
        secondary=instance_table,
        primaryjoin=instance_table.c.is_instance == id,
        secondaryjoin=instance_table.c.of == id,
        backref="instances",
    )

    @classmethod
    def from_visitor(cls, visitor):
        return cls(
            id=visitor.id,
            name=visitor.label,
            description=visitor.description,
            sitelink=visitor.wikipedia_link,
            claims=visitor.claims,
        )

    def __str__(self):
        return f"Q{self.id}: {self.name} ({self.sitelink})"

    @property
    def claim_dict(self):
        return json.loads(self.claims)
