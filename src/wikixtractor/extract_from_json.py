import argparse
import json
import pickle

from bz2 import BZ2File
from pprint import pprint

# with open("wiki_data/properties.pkl", "rb") as props:
#     properties_mapper = pickle.load(props)

properties_mapper = {}

properties_mapper.update(
    {
        "Q6581097": "male",
        "Q6581072": "female",
    }
)


def parse_person(data):
    item_id = data["id"]

    # Try to get the label
    labels = data["labels"]
    if "en" in labels:
        label = labels["en"]["value"]
    else:
        # If there's no english label, bail out
        return None

    # Try to get the description
    descriptions = data["descriptions"]
    if "en" in descriptions:
        description = descriptions["en"]["value"]
    else:
        description = ""

    claims = data["claims"]

    print(f"{label.ljust(20)} ({str(item_id).ljust(12)}):", description)

    # Try to get the gender
    gender_id = claims["P21"][0]["mainsnak"]["datavalue"]["value"]["id"]

    # Try to get date of birth
    dob = claims["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]

    # Try to get date of death
    if "P570" in claims:
        dod = claims["P570"][0]["mainsnak"]["datavalue"]["value"]["time"]
    else:
        dod = None

    print(" -", properties_mapper.get(gender_id, gender_id))
    print(" - ", dob, "::", dod)


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
            categories.add(snak["datavalue"]["value"]["id"])
        if "Q5" in categories:  # A human!
            parse_person(data)


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

    with BZ2File(args.data_file_name) as f:
        for line_num, line in enumerate(f):
            try:
                parse(line)
            except Exception as e:
                print("Error parsing line", f"{line_num} - {type(e).__name__}: {e}")
            if line_num >= 200:
                break


if __name__ == "__main__":
    main()
