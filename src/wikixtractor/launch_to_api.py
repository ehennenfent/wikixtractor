import argparse
import time

import orjson as json

from progressbar import progressbar

from src.api.client import ApiClient
from src.api.models import Entity
from src.db import Session
from src.db.models import Item, InstanceRecord, instance_table
from src.utils import RealItems, NotRealItems
from src.utils.visit_entry import EntityId
from sqlalchemy import or_

INTERVAL = 100  # 10_000


def main():
    parser = argparse.ArgumentParser(description="Upload data to botticelli API")
    parser.add_argument(
        "password",
        type=str,
        help="API password",
    )

    args = parser.parse_args()
    session = Session()

    ids = {EntityId.parse(i).id for i in RealItems | NotRealItems}
    ids.remove(5)

    # for thingy in (
    #     session.query(Item)
    #     .filter(Item.instance_of.any(Item.id.in_(ids)))
    #     .order_by(Item.views.desc())
    #     .limit(10)
    # ):
    #     print(thingy)

    base_query = (
        session.query(Item)
        .join(InstanceRecord, Item.id == InstanceRecord.is_instance)
        .filter(Item.sitelink != None)
        .filter(Item.views > 0)
        .filter(or_(InstanceRecord.of == j for j in ids))
        .order_by(Item.views.desc())
    )

    retrieved = set()
    for item in base_query.yield_per(100):
        entity = Entity.from_item_with_session(item, session)
        if entity not in retrieved:
            print(item)
        retrieved.add(entity)
        if len(retrieved) > INTERVAL:
            break

    # with open("top_20k_humans.json", "w") as outf:
    #     outf.write(
    #         json.dumps(
    #             list(sorted(retrieved, key=lambda e: e.score, reverse=True))
    #         ).decode("utf-8")
    #     )

    client = ApiClient()
    client.authorize("wikibot", args.password)

    for e in list(sorted(retrieved, key=lambda e: e.score, reverse=True)):
        time.sleep(1)
        client.upload_entity(e)


if __name__ == "__main__":
    main()
