import enum
from sqlalchemy import Table, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, Enum

from . import Base

class Gender(enum.Enum):
    Male = 1
    Female = 2
    NB_other = 0

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    score = Column(Integer, default=0)
    birth_year = Column(Integer)
    gender = Column(Enum(Gender))
    is_real = Column(Boolean)
    is_living = Column(Boolean)


class Trait(Base):
    __tablename__ = "traits"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    value = Column(Boolean)

trait_associationas = Table("has_traits", Base.metadata,
    Column("person_id", Integer, ForeignKey("people.id")),
    Column("trait_id", Integer, ForeignKey("traits.id"))
)
