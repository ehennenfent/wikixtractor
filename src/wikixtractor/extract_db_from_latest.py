import argparse
import json

from src.db import Session
from src.db.models import Property, Item

from bz2 import BZ2File
from progressbar import progressbar

from src.wikixtractor.visit_entry import PropertyVisitor, parse, ItemVisitor


def main():
    parser = argparse.ArgumentParser(
        description="Extract data from BZ2 compressed JSON file"
    )
    parser.add_argument(
        "data_file_name",
        type=str,
        help="JSON file with one entry per line",
    )

    args = parser.parse_args()
    interval = 10_000

    with BZ2File(args.data_file_name) as f:
        session = Session()

        for line_num, line in progressbar(enumerate(f)):
            try:
                parsed_entity = parse(line)
                if isinstance(parsed_entity, PropertyVisitor):
                    session.merge(Property.from_visitor(parsed_entity))
                elif isinstance(parsed_entity, ItemVisitor):
                    if parsed_entity.wikipedia_link is not None:
                        session.merge(Item.from_visitor(parsed_entity))
            except Exception as e:
                print("\nError parsing line", f"{line_num} - {type(e).__name__}: {e}")
            if (line_num + 1) % interval == 0:
                session.commit()
        session.commit()

if __name__ == "__main__":
    main()
