from enum import Enum as _Enum

from .CachedData import CachedList
from .visitor import Visitor


class Id(_Enum):
    INSTANCE_OF = "P31"
    HUMAN = "Q5"
