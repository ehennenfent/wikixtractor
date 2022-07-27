from dataclasses import dataclass, field
import enum
import typing as t
from hashlib import md5

from src.db import Item
from src.utils import RealItems, NotRealItems, Id
from src.utils.extract_features import extract_tags
from src.utils.visit_entry import EntityId
from urllib.parse import quote


def get_image_url(fname):
    fname = fname.replace(" ", "_")
    hashed = md5(fname.encode("utf-8")).hexdigest()
    hash1 = hashed[:1]
    hash2 = hashed[:2]

    return (
        f"https://upload.wikimedia.org/wikipedia/commons/{hash1}/{hash2}/{quote(fname)}"
    )


def check_is_real(instance_of: t.Set[str]) -> bool:
    realness = instance_of & RealItems
    not_realness = instance_of & NotRealItems
    if realness:
        return True
    if not_realness:
        return False
    raise RuntimeError(
        f"Don't know how to tell whether {instance_of}, represents a real item"
    )


def check_if_equal(expected: EntityId, maybe_item):
    if isinstance(maybe_item, Item):
        return expected == maybe_item.entity_id
    if isinstance(maybe_item, EntityId):
        return expected == maybe_item
    if isinstance(maybe_item, str):
        return str(expected) == maybe_item
    return expected == maybe_item


def always_to_str(maybe_item):
    if isinstance(maybe_item, Item):
        return maybe_item.name
    return str(maybe_item)


class Gender(enum.Enum):
    male = "male"
    female = "female"
    analog = "analog"
    null = "null"


@dataclass
class Entity:
    wikidata_id: str
    is_real: bool
    is_living: bool
    given_name: str = field(default="")
    nickname: str = field(default="")
    surname: str = field(default="")
    birth_year: str = field(default="")
    death_year: str = field(default="")
    gender: Gender = field(default=Gender.null)
    score: int = field(default=0)
    description: str = field(default="")
    wikipedia_url: str = field(default="")
    image_url: str = field(default="")
    tags: t.List[str] = field(default_factory=list)
    facts: t.List[str] = field(default_factory=list)

    def __hash__(self):
        return hash((self.wikidata_id, self.given_name))

    @classmethod
    def from_item_with_session(cls, item: Item, session):

        rich_claims = item.rich_claims(session)

        is_real = check_is_real(item.instance_of_tags)
        is_living = False if not is_real else Id.DATE_OF_DEATH.value not in rich_claims

        entity = cls(
            wikidata_id=f"Q{item.id}",
            is_real=is_real,
            is_living=is_living,
            score=item.views,
            description=item.description,
            wikipedia_url=f"https://en.wikipedia.org/w/index.php?title={quote(item.sitelink)}"
            if item.sitelink is not None
            else "",
            tags=extract_tags(item, rich_claims),
        )

        # name
        if Id.PSEUDONYM.value in rich_claims:
            entity.nickname = always_to_str(rich_claims[Id.PSEUDONYM.value][0])
        if Id.FAMILY_NAME.value in rich_claims:
            entity.surname = always_to_str(rich_claims[Id.FAMILY_NAME.value][0])
        if Id.GIVEN_NAME.value in rich_claims:
            maybe_given_name = always_to_str(rich_claims[Id.GIVEN_NAME.value][0])
            entity.given_name = (
                maybe_given_name if maybe_given_name is not None else item.name
            )
        else:
            entity.given_name = item.name

        # birth/death
        if Id.DATE_OF_BIRTH.value in rich_claims:
            entity.birth_year = rich_claims[Id.DATE_OF_BIRTH.value][0]
        if Id.DATE_OF_DEATH.value in rich_claims:
            entity.death_year = rich_claims[Id.DATE_OF_DEATH.value][0]

        # gender
        if Id.SEX_OR_GENDER.value in rich_claims:
            gender = rich_claims[Id.SEX_OR_GENDER.value][
                -1
            ]  # hopefully these go chronologically
            if check_if_equal(EntityId.parse(Id.MALE.value), gender):
                entity.gender = Gender.male
            elif check_if_equal(EntityId.parse(Id.FEMALE.value), gender):
                entity.gender = Gender.female
            else:
                entity.gender = Gender.analog

        # image
        for fname in rich_claims.get(Id.IMAGE.value, [])[:1]:
            if fname is not None:
                entity.image_url = get_image_url(fname)

        return entity
