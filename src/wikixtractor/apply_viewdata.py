import argparse

from progressbar import progressbar

from src.db import Session
from src.db.models import Item

INTERVAL = 10_000


def parse_pageview(line):
    wikicode, rest = tuple(line.split(" ", 1))
    title, rest = tuple(rest.split(" ", 1))
    _page_id, rest = tuple(rest.split(" ", 1))
    _source, rest = tuple(rest.split(" ", 1))
    views, rest = tuple(rest.split(" ", 1))
    return wikicode, title, int(views)


def main():
    parser = argparse.ArgumentParser(
        description="Apply view data from filtered text file"
    )
    parser.add_argument(
        "data_file_name",
        type=str,
        help="text file with one entry per line",
    )

    args = parser.parse_args()

    with open(args.data_file_name, "rb") as f:
        session = Session()

        num_processed = 0
        for line_num, line in progressbar(enumerate(f)):
            try:
                wikicode, title, daily_total = parse_pageview(line.strip().decode("utf-8"))

                if wikicode == "en.wikipedia":
                    row = session.query(Item).filter(Item.sitelink == title).first()
                    if row is not None:
                        row.views = row.views + daily_total
                        num_processed += 1

            except Exception as e:
                print("\nError parsing line", f"{line_num} - {type(e).__name__}: {e}")
            if (num_processed + 1) % INTERVAL == 0:
                session.commit()
        session.commit()

    bilbo = session.query(Item).get(185737)
    print(bilbo)


if __name__ == "__main__":
    main()
