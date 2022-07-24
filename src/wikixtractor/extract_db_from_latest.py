import argparse
from queue import Queue

from src.db import Session, engine
from src.db.models import Property, Item, RankData, instance_table, InstanceRecord

from bz2 import BZ2File
from progressbar import progressbar

from src.utils import Id
from src.wikixtractor.visit_entry import PropertyVisitor, parse, ItemVisitor, ClaimVisitor, EntityId

parsed_lines =

def parse_instance_of(entity: ItemVisitor):
    already_seen = set()
    instance_of = entity.claims.pop(Id.INSTANCE_OF.value, [])
    for claim in instance_of:
        parsed = ClaimVisitor().visit(claim).data.value
        if isinstance(parsed, EntityId):
            if parsed.type == "Q":
                if parsed.id not in already_seen:
                    already_seen.add(parsed.id)
                    yield InstanceRecord(is_instance=entity.id, of=parsed.id)


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
    interval = 300

    with BZ2File(args.data_file_name) as f:
        session = Session()
        for line_num, line in progressbar(enumerate(f)):
            try:
                parsed_entity = parse(line)
                if isinstance(parsed_entity, PropertyVisitor):
                    session.add(Property.from_visitor(parsed_entity))
                elif isinstance(parsed_entity, ItemVisitor):
                    for instance_record in parse_instance_of(parsed_entity):
                        session.add(instance_record)
                    if parsed_entity.wikipedia_link is None:
                        parsed_entity.claims = {}
                    session.add(Item.from_visitor(parsed_entity))
            except Exception as e:
                print("\nError parsing line", f"{line_num} - {type(e).__name__}: {e}")
            if (line_num + 1) % interval == 0:
                session.commit()
            if line_num > 1000:
                break
        session.commit()

    print(session.query(Item).get(42))

if __name__ == "__main__":
    main()
