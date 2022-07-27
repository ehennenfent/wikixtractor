from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON

from . import Base
import orjson as json

from ..utils.visit_entry import ClaimVisitor, EntityId

instance_table = Table(
    "instance_of",
    Base.metadata,
    Column("of", ForeignKey("items.id"), primary_key=True, autoincrement=False),
    Column(
        "is_instance", ForeignKey("items.id"), primary_key=True, autoincrement=False
    ),
)

_instance_idx = Index("instance_idx", instance_table.c.of, instance_table.c.is_instance)
_instance_rev_idx = Index(
    "instance_rev_idx", instance_table.c.is_instance, instance_table.c.of
)


class InstanceRecord(Base):
    __table__ = instance_table

    def __str__(self):
        return f"{self.of}: {self.is_instance}"


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
        return f"Q{self.id}: {self.name} ({self.description}) [{self.views}]"

    @property
    def claim_dict(self):
        return json.loads(self.claims)

    @property
    def instance_of_tags(self):
        return {f"Q{i.id}" for i in self.instance_of}

    def rich_claims(self, session):
        rich_claims = {}

        raw_claims = self.claims
        for k in raw_claims:
            rich_claims[k] = [visit_claim(c, session) for c in raw_claims[k]]
        return rich_claims

    @property
    def entity_id(self):
        return EntityId("Q", self.id)


def visit_claim(claim, session):
    claim = ClaimVisitor().visit(claim)
    if claim.data is None:
        return None
    value = claim.data.value
    if isinstance(value, EntityId):
        queried = session.query(Item).get(value.id)
        return queried if queried is not None else value
    return value
