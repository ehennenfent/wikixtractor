import argparse
from progressbar import progressbar
from functools import partial
from itertools import tee
from bz2 import decompress


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def slugify(slug_me: str) -> str:
    return slug_me.strip().replace(" ", "_")


def parse_index(index_file):
    offsets = set()
    offset_sizes = {}
    article_data = {}

    for line in progressbar(index_file):
        tokens = line.strip().split(":")
        offset = int(tokens[0])
        article_id = int(tokens[1])
        rest = ":".join(tokens[2:])

        offsets.add(offset)
        article_data[slugify(rest)] = (offset, article_id)

    for smaller, larger in pairwise(sorted(offsets)):
        offset_sizes[smaller] = larger - smaller
        offset_sizes[larger] = -1

    return offset_sizes, article_data


def _extract(offset_sizes, article_data, data_file, title):
    slug = slugify(title)
    if slug not in article_data:
        print("No article found entitled:", title)
        return
    offset, article_id = article_data[slug]
    data_file.seek(offset)
    compressed_data = data_file.read(offset_sizes[offset])
    with open(f"{slug}_stream.txt", "wb") as stream_out:
        stream_out.write(b"<data>\n")
        stream_out.write(decompress(compressed_data))
        stream_out.write(b"</data>\n")


def main():
    parser = argparse.ArgumentParser(
        description="Extract data from compressed multistream BZ2 archive"
    )
    parser.add_argument(
        "index_file",
        type=argparse.FileType("r"),
        help="Text file with article offset information",
    )
    parser.add_argument(
        "archive_file",
        type=argparse.FileType("rb"),
        help="Compressed multistream BZ2 archive containing page data",
    )

    args = parser.parse_args()

    extract = partial(_extract, *parse_index(args.index_file), args.archive_file)

    while (title := input("> ")) != "exit":
        extract(title)


if __name__ == "__main__":
    run()
