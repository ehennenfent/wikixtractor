import orjson as json
import typing as t
from dataclasses import dataclass

from src.utils.visitor import Visitor


def slug_encode(slug):
    return slug.replace(" ", "_")


@dataclass
class EntityId:
    type: str
    id: int

    @classmethod
    def parse(cls, encoded):
        if encoded[0] == "L":
            return None
        return cls(type=encoded[0], id=int(encoded[1:]))

    def __hash__(self):
        return hash((self.type, self.id))

    def __str__(self):
        return f"{self.type}{self.id}"


class SnakVisitor(Visitor):
    def __init__(self):
        self.property = None
        self.snak_type = None
        self.data_type = None
        self.value = None

    def visit_property(self, prop):
        self.property = EntityId.parse(prop)

    def visit_snaktype(self, ty):
        self.snak_type = ty

    def visit_datatype(self, ty):
        self.data_type = ty

    def visit_datavalue(self, val):
        ty = val["type"]
        if ty == "string":
            self.value = val["value"]
        elif ty == "wikibase-entityid":
            self.value = EntityId.parse(val["value"]["id"])
        elif ty == "monolingualtext":
            self.value = val["value"]["text"]
        elif ty == "time":
            self.value = val["value"]["time"]
        elif ty == "quantity":
            self.value = val["value"]["amount"]  # TODO: add units
        elif ty in ("globecoordinate", "multilingualtext"):
            self.value = str(val)

    def __str__(self):
        return f"  - {self.property}: {self.value}"


class ClaimVisitor(Visitor):
    def __init__(self):
        self.data = None

    def visit_mainsnak(self, snak):
        self.data = SnakVisitor().visit(snak)

    def __str__(self):
        return str(self.data)


class EntityVisitor(Visitor):
    def __init__(self) -> None:
        super().__init__()
        self.page_id = None
        self.label = None
        self.id = None
        self.description = None
        self.claims = {}

    def visit_pageid(self, page_id):
        self.page_id = page_id

    def visit_labels(self, labels):
        self.label = labels.get("en", {}).get("value", None)

    def visit_id(self, item_id):
        self.id = int(item_id[1:])

    def visit_descriptions(self, descriptions):
        self.description = descriptions.get("en", {}).get("value", None)

    def visit_claims(self, claims):
        for key, value in claims.items():
            self.claims[key] = value  # [ClaimVisitor().visit(c) for c in value]


class PropertyVisitor(EntityVisitor):
    pass


class ItemVisitor(EntityVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.wikipedia_link = None

    def visit_sitelinks(self, site_links):
        wiki_data = site_links.get("enwiki", {})
        if "url" in wiki_data:
            self.wikipedia_link = wiki_data.get("url").split(
                "en.wikipedia.org/w/index.php?title="
            )[-1]
        elif "title" in wiki_data:
            self.wikipedia_link = slug_encode(wiki_data.get("title"))

    def __str__(self):
        return "\n".join(
            [
                f"{self.label.ljust(20)} ({str(self.id).ljust(12)}): {self.description}",
                *(str(claim) for claim in self.claims.values()),
            ]
        )


def parse_entry(entry: t.Dict):
    ty = entry["type"]
    if ty == "item":
        return ItemVisitor().visit(entry)
    elif ty == "property":
        return PropertyVisitor().visit(entry)


def parse(line):
    return parse_entry(json.loads(line.strip().rstrip(b",")))
