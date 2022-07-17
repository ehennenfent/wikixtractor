import argparse
import json
import pickle

from bz2 import BZ2File
from pprint import pprint
from progressbar import progressbar

from wiki_data import id_to_label, views

def slug_encode(slug):
    return slug.replace(" ", "_")

class Visitor:
    def visit(self, visit_me):
        for key in visit_me:
            if hasattr(self, f"visit_{key}"):
              getattr(self, f"visit_{key}")(visit_me[key])
        return self

class SnakVisitor(Visitor):
    def __init__(self):
        self.property = None
        self.snak_type = None
        self.data_type = None
        self.value = None

    def visit_property(self, prop):
        wiki_ty = prop[0]
        wiki_id = int(prop[1:])
        self.property = id_to_label[wiki_ty][wiki_id]
    
    def visit_snaktype(self, ty):
        self.snak_type = ty
    
    def visit_datatype(self, ty):
        self.data_type = ty

    def visit_datavalue(self, val):
        ty = val["type"]
        if ty == "string":
            self.value = val["value"]
        elif ty == "wikibase-entityid":
            try:
                wiki_ty = val["value"]["id"][0]
                wiki_id = int(val["value"]["id"][1:])
                self.value = id_to_label.get(wiki_ty, {}).get(wiki_id, val["value"]["id"])
            except ValueError:
                self.value = val["value"]["id"]
        elif ty == "monolingualtext":
            self.value = val["value"]["text"]
        elif ty == "time":
            self.value = val["value"]["time"]
        elif ty == "quantity":
            self.value = val["value"]["amount"] # TODO: add units
        elif ty in ("globecoordinate"):
            self.value = str(val)
        else:
            self.value == None

    def __str__(self):
        return f"  - {self.property}: {self.value}"

class ClaimVisitor(Visitor):
    def __init__(self):
        self.data = None

    def visit_mainsnak(self, snak):
        self.data = SnakVisitor().visit(snak)

    def __str__(self):
        return str(self.data)

class PersonVisitor(Visitor):
    def __init__(self) -> None:
        super().__init__()
        self.page_id = None
        self.label = None
        self.id = None
        self.description = None
        self.wikipedia_link = None
        self.views = None
        self.claims = {}

    def visit_pageid(self, page_id):
        self.page_id = page_id

    def visit_labels(self, labels):
        self.label = labels.get("en", {}).get("value", None)

    def visit_id(self, item_id):
        self.id = item_id
    
    def visit_descriptions(self, descriptions):
        self.description = descriptions.get("en", {}).get("value", None)

    def visit_sitelinks(self, site_links):
        wiki_data = site_links.get("enwiki", {})
        if "url" in wiki_data:
            self.wikipedia_link = wiki_data.get("url")
            key = self.wikipedia_link.split("en.wikipedia.org/wiki/")[-1]
            self.views = views.get(key, None)
        elif "title" in wiki_data:
            slug = slug_encode(wiki_data.get("title"))
            self.views = views.get(slug, None)
            self.wikipedia_link = f"https://en.wikipedia.org/w/index.php?title={slug}"

    def visit_claims(self, claims):
        for key, value in claims.items():
            ty = key[0]
            val = int(key[1:])
            cat = id_to_label[ty][val]
            if (l:= len(value) == 1):
                self.claims[cat] = ClaimVisitor().visit(value[0])
            if l > 1:
                self.claims[cat] = [ClaimVisitor().visit(c) for c in value]


    def __str__(self):
        return "\n".join([
            f"{self.label.ljust(20)} ({str(self.id).ljust(12)}): {self.description}",
            f"with {self.views} hits at {self.wikipedia_link}",
            *(str(claim) for claim in self.claims.values())
        ])


def parse(line):
    data = json.loads(line.strip().rstrip(b","))
    ty = data["type"]
    if ty == "item":
        categories = set()
        claims = data["claims"]
        if "P31" not in claims:  # If this isn't an instance of anything, ignore it
            return
        for cat in claims["P31"]:  # Find all the things this is an instance of
            snak = cat["mainsnak"]
            categories.add(snak['datavalue']['value']['id'])
        if "Q5" in categories:  # A human!
            return PersonVisitor().visit(data)

def main():
    parser = argparse.ArgumentParser(
        description="Extract data from uncompressed JSON file"
    )
    parser.add_argument(
        "data_file_name",
        type=str,
        help="JSON file with one entry per line",
    )

    args = parser.parse_args()

    people = []
    interval = 3_000_000

    with BZ2File(args.data_file_name) as f:
        for line_num, line in progressbar(enumerate(f)):
            try:
                person = parse(line)
                if person.wikipedia_link is not None:
                    people.append(person)
            except Exception as e:
                # raise e
                print("Error parsing line", f"{line_num} - {type(e).__name__}: {e}")
            # if line_num >= 2:
            #     break
            if line_num % interval == 0:
                with open(f"people_with_wikipedia_unsorted_{line_num // interval}.pkl", "wb") as pkf:
                    pickle.dump(people, pkf)
                    people.clear()

    with open(f"people_with_wikipedia_unsorted_final.pkl", "wb") as pkf:
        pickle.dump(people, pkf)

    # del id_to_label
    # del views

    # people.sort(key=lambda p: p.views, reverse=True)

    # with open(f"people_with_wikipedia.pkl", "wb") as pkf:
    #     pickle.dump(people, pkf)

if __name__ == "__main__":
    main()
