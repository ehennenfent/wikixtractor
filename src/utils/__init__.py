from enum import Enum as _Enum

from .CachedData import CachedList
from .visitor import Visitor


class Id(_Enum):
    INSTANCE_OF = "P31"

    # Types of instances
    HUMAN = "Q5"

    # Related to names
    GIVEN_NAME = "P735"
    FAMILY_NAME = "P734"
    PSEUDONYM = "P742"

    # sex/gender
    SEX_OR_GENDER = "P21"
    SEXUAL_ORIENTATION = "P91"
    HETEROSEXUALITY = "Q1035954"
    MALE = "Q6581097"
    FEMALE = "Q6581072"

    # birth/death
    DATE_OF_BIRTH = "P569"
    DATE_OF_DEATH = "P570"

    # Demographics
    ETHNIC_GROUP = "P172"
    CITIZEN_OF_COUNTRY = "P27"
    FROM_NARRATIVE_UNIVERSE = "P1080"
    PRESENT_IN_WORK = "P1441"
    OCCUPATION = "P106"

    IMAGE = "P18"

    AWARD_RECEIVED = "P166"


RealItems = {
    Id.HUMAN.value,
    "Q726",  # horse
    "Q144",  # dog
    "Q146",  # house cat
    "Q26401003",  # "individual animal"
}

NotRealItems = {
    "Q15711870",  # animated character
    "Q3658341",  # literary character
    "Q15773347",  # film character
    "Q80447738",  # anime character
    "Q15773317",  # television character
    "Q1114461",  # comics book character
    "Q1569167",  # video game character
    "Q15632617",  # fictional human
    "Q27120684",  # fictional cat
    "Q15720625",  # fictional dog
    "Q1307329",  # fictional alien
    "Q16513881",  # norse deity
    "Q11688446",  # roman deity
    "Q22989102",  # greek deity
}
