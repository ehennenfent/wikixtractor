from src.db import Item
from src.utils import Id
from src.utils.visit_entry import EntityId


def entity_id_from(claim):
    if isinstance(claim, Item):
        return claim.entity_id
    if isinstance(claim, EntityId):
        return claim
    if isinstance(claim, str):
        return claim
    return None


professions = {
    "Q33999": "Actor",  # actor
    "Q10800557": "Actor",  # film actor
    "Q10798782": "Actor",  # television actor
    "Q2259451": "Actor",  # stage actor
    "Q2405480": "Actor",  # voice actor
    "Q483501": "Artist",  # artist
    "Q1028181": "Artist",  # painter
    "Q1281618": "Artist",  # sculptor
    "Q33231": "Artist",  # photographer
    "Q2526255": "Artist",  # film director
    "Q5716684": "Artist",  # dancer
    "Q2066131": "Athlete",  # athlete
    "Q3665646": "Athlete",  # basketball player
    "Q11774891": "Athlete",  # hockey player
    "Q10833314": "Athlete",  # tennis player
    "Q19204627": "Athlete",  # football player
    "Q937857": "Athlete",  # soccer player
    "Q11338576": "Athlete",  # boxer
    "Q36180": "Author",  # author (writer)
    "Q482980": "Author",  # writer
    "Q6625963": "Author",  # novelist
    "Q11774202": "Author",  # essayist
    "Q1930187": "Author",  # journalist
    "Q42909": "Author",  # reporter
    "Q49757": "Author",  # poet
    "Q214917": "Author",  # playwright
    "Q28389": "Author",  # screenwriter
    "Q639669": "Musician",  # musician
    "Q488205": "Musician",  # singer-songwriter
    "Q855091": "Musician",  # guitarist
    "Q486748": "Musician",  # pianist
    "Q177220": "Musician",  # singer
    "Q2252262": "Musician",  # rapper
    "Q36834": "Musician",  # composer
    "Q82955": "Politician",  # politician
    "Q372436": "Politician",  # statesperson
    "Q15995642": "Religious Figure",  # religious leader
    "Q1234713": "Religious Figure",  # theologian
    "Q152002": "Religious Figure",  # pastor
    "Q133485": "Religious Figure",  # rabbi
    "Q125482": "Religious Figure",  # imam
    "Q97722086": "Religious Figure",  # monk (western)
    "Q854997": "Religious Figure",  # monk (buddhist)
    "Q42857": "Religious Figure",  # prophet
    "Q42603": "Religious Figure",  # priest
    "Q250867": "Religious Figure",  # catholic priest
    "Q1469535": "Religious Figure",  # roman catholic priest
    "Q831474": "Religious Figure",  # christian priest
    "Q2259532": "Religious Figure",  # cleric
    "Q191421": "Religious Figure",  # lama
    "Q55631411": "Religious Figure",  # religious sister
    "Q191808": "Religious Figure",  # nun
    "Q1349880": "Religious Figure",  # miracle worker
    "Q901": "Scientist",  # scientist
    "Q593644": "Scientist",  # chemist
    "Q11063": "Scientist",  # astronomer
    "Q170790": "Scientist",  # mathematician
    "Q2374149": "Scientist",  # botanist
    "Q350979": "Scientist",  # zoologist
    "Q520549": "Scientist",  # geologist
    "Q864503": "Scientist",  # biologist
    "Q169470": "Scientist",  # physicist
    "Q16745601": "Scientist",  # quantum physicist
    "Q188094": "Scientist",  # economist
    "Q2310145": "Scientist",  # meteorologist
    "Q81096": "Engineer",  # engineer
    "Q42973": "Engineer",  # architect
    "Q13582652": "Engineer",  # civil engineer
    "Q21002336": "Engineer",  # nuclear engineer
    "Q10497074": "Engineer",  # aerospace engineer
    "Q1326886": "Engineer",  # electrical engineer
    "Q7888586": "Engineer",  # chemical engineer
    "Q151197": "Engineer",  # military engineer
    "Q43845": "Business Person",  # businessperson
    "Q557880": "Business Person",  # investor
    "Q911554": "Business Person",  # business magnate
    "Q1979607": "Business Person",  # financier
    "Q806798": "Business Person",  # banker
    "Q131524": "Business Person",  # entrepreneur
    "Q47064": "Military Figure",  # military personnel
    "Q189290": "Military Figure",  # military officer
    "Q4991371": "Military Figure",  # soldier
    "Q1397808": "Military Figure",  # resistance fighter
    "Q2045208": "Personality",  # internet celebrity
    "Q512314": "Personality",  # socialite
    "Q211236": "Personality",  # celebrity
    "Q44508716": "Personality",  # television personality
    "Q2722764": "Personality",  # radio personality
    "Q8246794": "Personality",  # blogger
    "Q15077007": "Personality",  # podcaster
    "Q17125263": "Personality",  # youtuber
    "Q4964182": "Philosopher",  # philosopher
    "Q15994177": "Philosopher",  # political theorist
    "Q3400985": "Academic",  # academic
    "Q1622272": "Academic",  # university teacher
    "Q121594": "Academic",  # professor
    "Q201788": "Academic",  # historian
    "Q82594": "Computer Scientist",  # Computer scientist
    "Q5482740": "Computer Scientist",  # programmer
    "Q188784": "Superhero",  # superhero
    "Q205375": "Inventor",  # inventor
    "Q40348": "Lawyer",  # lawyer
    "Q39631": "Physician",  # physician
    "Q156839": "Chef",  # cook
    "Q10076267": "Slave Owner",  # slave owner
    "Q11631": "Astronaut",  # astronaut
}

countries_and_civs = {
    "Q30": "American",  # USA! USA!
    "Q29": "Spanish",
    "Q183": "German",
    "Q43287": "German",
    "Q41304": "German",
    "Q1206012": "German",
    "Q142": "French",
    "Q71084": "French",
    "Q79": "Egyptian",
    "Q11768": "Egyptian",
    "Q12544": "Byzantine",
    "Q145": "UK-ish",
    "Q179876": "English",
    "Q41": "Greek",
    "Q4420718": "Greek",
    "Q844930": "Greek",
    "Q1747689": "Roman",
    "Q27": "Irish",
    "Q148": "Chinese",
    "Q9903": "Chinese",
    "Q736936": "Chinese",
    "Q884": "Korean",
    "Q17": "Japanese",
    "Q668": "Indian",
    "Q83618": "Indian",
    "Q38": "Italy",
    "Q22": "Scottish",
    "Q843": "Pakistani",
    "Q928": "Filipino",
    "Q159": "Russian",
    "Q15180": "Russian",
}

# This list is incomplete. You can help by expanding it ig
ethnic_groups = {
    "Q49085": "African American",
    "Q161652": "Japanese",
    "Q49297": "Indigenous American",
    "Q49542": "Russian",
    "Q1282294": "South Asian",
    "Q854323": "South Asian",
}

awards = {
    "Q35637": "Nobel Prize",  # Nobel peace prize
    "Q37922": "Nobel Prize",  # Nobel prize in literature
    "Q80061": "Nobel Prize",  # Nobel prize in medicine
    "Q44585": "Nobel Prize",  # Nobel prize in chemistry
    "Q38104": "Nobel Prize",  # Nobel prize in physics
    "Q47170": "Nobel Prize",  # Nobel prize in economics
    "Q203535": "Medal of Honor",
    "Q17144": "Medal of Freedom",
    "Q737051": "National Medal of Science",
    "Q207826": "Time Person of the Year",
    "Q103360": "Academy Award",  # best director
    "Q103916": "Academy Award",  # best actor
    "Q106291": "Academy Award",  # best supporting actor
    "Q103618": "Academy Award",  # best actress
    "Q106301": "Academy Award",  # best supporting actress
    "Q5593890": "Grammy",  # spoken word album
    "Q1453643": "Grammy",  # new artist
    "Q904528": "Grammy",  # album of the year
    "Q1027904": "Grammy",  # song of the year
    "Q843219": "Grammy",  # record of the year
    "Q691892": "Grammy",  # rock album of the year
    "Q1542129": "Grammy",  # alt music album of the year
    "Q1367988": "Grammy",  # rap album of the year
    "Q28835": "Fields Medal",
    "Q185667": "Turing Award",
    "Q15243387": "Olympic Medal",  # gold
    "Q15889641": "Olympic Medal",  # silver
    "Q15889643": "Olympic Medal",  # bronze
    "Q46525": "Pulitzer Prize",  # pulitzer
    "Q833633": "Pulitzer Prize",  # fiction
    "Q289214": "Pulitzer Prize",  # drama
    "Q2117891": "Pulitzer Prize",  # poetry
    "Q599254": "Pulitzer Prize",  # history
    "Q285117": "Pulitzer Prize",  # biography
    "Q463085": "Golden Globe",  # best actress
    "Q1257501": "Golden Globe",  # best actress (tv)
    "Q822907": "Golden Globe",  # best supporting actress
    "Q593098": "Golden Globe",  # best actor
    "Q1257493": "Golden Globe",  # best actor (tv)
    "Q723830": "Golden Globe",  # best supporting actor
    "Q586356": "Golden Globe",  # best director
}

non_humans = {
    "Q726": "Horse",
    "Q2962925": "Horse",
    "Q144": "Dog",
    "Q15720625": "Dog",
    "Q146": "Cat",
    "Q27120684": "Cat",
    "Q1307329": "Alien",
    "Q16513881": "Deity",  # norse
    "Q11688446": "Deity",  # roman
    "Q22989102": "Deity",  # greek
    "Q979507": "Deity",  # hindu
}

fictional_universe = {
    "Q81738": "Tolkien Legendarium",
    "Q208002": "Tolkien Legendarium",
    "Q131074": "Tolkien Legendarium",
    "Q15228": "Tolkien Legendarium",
    "Q74287": "Tolkien Legendarium",
    "Q79762": "Tolkien Legendarium",
    "Q309019": "Tolkien Legendarium",
    "Q11679": "Hunger Games",
    "Q748351": "Hunger Games",
    "Q931597": "Marvel Cinematic Universe",
    "Q1152150": "DC Universe",
    "Q19610143": "The Expanse",
    "Q18389644": "The Expanse",
    "Q18043309": "Star Trek",
    "Q1077": "Star Trek",  # Original
    "Q16290": "Star Trek",  # TNG
    "Q108774": "Star Trek",  # DS9
    "Q156329": "Star Trek",  # Voyager
    "Q19786052": "Star Wars",
    "Q462": "Star Wars",
    "Q42051": "Star Wars",
    "Q17738": "Star Wars",
    "Q181795": "Star Wars",
    "Q181803": "Star Wars",
    "Q6074": "Star Wars",
    "Q18486021": "Star Wars",
    "Q165713": "Star Wars",
    "Q1989642": "The Witcher",
    "Q4267401": "The Witcher",
    "Q917272": "The Witcher",
    "Q11835640": "The Witcher",
    "Q2461698": "Game of Thrones",
    "Q23572": "Game of Thrones",
    "Q45875": "Game of Thrones",
    "Q501121": "Chronicles of Narnia",
    "Q1211909": "Chronicles of Narnia",
    "Q485093": "Chronicles of Narnia",
    "Q5410773": "Harry Potter",
    "Q102438": "Harry Potter",
    "Q102448": "Harry Potter",
    "Q102225": "Harry Potter",
    "Q102235": "Harry Potter",
    "Q161687": "Harry Potter",
}


def extract_tags(item: Item, claims):
    tags = set()

    # occupation/category
    for claim in claims.get(Id.OCCUPATION.value, []):
        key = str(entity_id_from(claim))
        if key in professions:
            tags.add(professions[key])

    # country of origin
    for claim in claims.get(Id.CITIZEN_OF_COUNTRY.value, []):
        key = str(entity_id_from(claim))
        if key in countries_and_civs:
            tags.add(countries_and_civs[key])

    # ethnic group
    for claim in claims.get(Id.ETHNIC_GROUP.value, []):
        key = str(entity_id_from(claim))
        if key in ethnic_groups:
            tags.add(ethnic_groups[key])

    # awards
    for claim in claims.get(Id.AWARD_RECEIVED.value, []):
        key = str(entity_id_from(claim))
        if key in awards:
            tags.add(awards[key])

    # instance of
    for instance_of in item.instance_of_tags:
        if instance_of in non_humans:
            tags.add(non_humans[instance_of])

    # fictional universe
    for claim in claims.get(Id.FROM_NARRATIVE_UNIVERSE.value, []):
        key = str(entity_id_from(claim))
        if key in fictional_universe:
            tags.add(fictional_universe[key])
    for claim in claims.get(Id.PRESENT_IN_WORK.value, []):
        key = str(entity_id_from(claim))
        if key in fictional_universe:
            tags.add(fictional_universe[key])

    # sexuality
    for claim in claims.get(Id.SEXUAL_ORIENTATION.value, []):
        key = str(entity_id_from(claim))
        if key != Id.HETEROSEXUALITY.value:
            tags.add("LGBTQ+")

    return list({"name": t} for t in tags)
