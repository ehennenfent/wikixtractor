import argparse
from bz2 import BZ2File
from queue import Queue, Empty
from threading import Thread

from progressbar import ProgressBar

from src.db import Session
from src.db.models import Property, Item, InstanceRecord
from src.utils import Id
from src.utils.visit_entry import (
    PropertyVisitor,
    parse,
    ItemVisitor,
    ClaimVisitor,
    EntityId,
)

MAX_LINES = 101_000_000
INTERVAL = 20_000
raw_lines = Queue(maxsize=INTERVAL * 25)


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


def read_bz2_file(fname):
    with BZ2File(fname) as f:
        for i, line in enumerate(f):
            raw_lines.put(line, block=True)
            if i > MAX_LINES:
                break


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

    reader_thread = Thread(target=read_bz2_file, args=(args.data_file_name,))
    reader_thread.start()

    session = Session()
    line_num = 0
    with ProgressBar(max_value=MAX_LINES + 1) as pbar:
        while True:
            try:
                line = raw_lines.get(block=True, timeout=30)
                try:
                    pbar.update(line_num)
                    line_num += 1
                    parsed_entity = parse(line)
                    if isinstance(parsed_entity, PropertyVisitor):
                        session.add(Property.from_visitor(parsed_entity))
                    elif isinstance(parsed_entity, ItemVisitor):
                        for instance_record in parse_instance_of(parsed_entity):
                            session.add(instance_record)
                        if parsed_entity.wikipedia_link is None:
                            parsed_entity.claims = {}
                        if (
                            parsed_entity.label is None
                            and parsed_entity.description is None
                        ):
                            continue
                        session.add(Item.from_visitor(parsed_entity))
                except Exception as e:
                    print(
                        "\nError parsing line", f"{line_num} - {type(e).__name__}: {e}"
                    )
                if (line_num + 1) % INTERVAL == 0:
                    pbar.update(line_num, force=True)
                    session.commit()
            except Empty:
                pbar.update(line_num, force=True)
                session.commit()
                break

    print(session.query(Item).get(42))


if __name__ == "__main__":
    main()
