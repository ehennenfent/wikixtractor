import pickle
from pathlib import Path
from bz2 import BZ2File
from io import BytesIO
from glob import glob
import typing as t
import os

ONE_GB = 1024 ** 3
CACHE_DIR = Path(__file__).parent.parent.joinpath("wiki_data", ".cache")


class CachedList:
    def __init__(
        self,
        name: str,
        regen_func: t.Callable,
        shard_size: int = ONE_GB,
        compress: bool = True,
    ):
        self.name = name
        self.shard_size = shard_size
        self.compress = compress
        self._buffer = BytesIO()
        self._in_memory = list()
        self._bytes_written = 0
        self._regen_func = regen_func

    def append(self, item: t.Any):
        """Add one item to the tracked store"""
        self._in_memory.append(item)
        self._bytes_written += self._buffer.write(pickle.dump(item))
        self._flush_if_too_large()

    def clear(self):
        self._in_memory.clear()
        self._buffer.close()
        self._buffer = BytesIO()
        self._bytes_written = 0
        for file in glob(str(self.make_path_for("*"))):
            os.remove(file)

    def save(self, iterable: t.Iterable):
        """Replace everything with the current contents"""
        self.flush()
        self.clear()
        for i in iterable:
            self.append(i)

    def regenerate(self):
        """Get the underlying data from scratch"""
        self._regen_func(self)
        self.flush()

    def get(self, force_regen=False):
        """Get the entire saved contents from the disk"""
        return list(i for i in self.stream(force_regen=force_regen))

    def generate_if_not_existing(self, force=False):
        if not glob(str(self.make_path_for("*"))) or force:
            self.regenerate()

    def stream(self, force_regen=False):
        """Yields successive cached items, loading more from the disk if we need to"""
        self.generate_if_not_existing(force=force_regen)
        existing = sorted(glob(str(self.make_path_for("*"))))

        if existing:
            for file in existing:
                if self.compress:
                    with BZ2File(file, "rb") as pkf:
                        while pkf.peek(1):
                            yield pickle.load(pkf)
                else:
                    with open(file, "rb") as pkf:
                        while pkf.peek(1):
                            yield pickle.load(pkf)
        else:
            for i in self._in_memory:
                yield i

    def _flush_if_too_large(self):
        if self._bytes_written > self.shard_size:
            self.flush()

    def flush(self):
        """Save any remaining in-memory data to disk"""
        if self.compress:
            with BZ2File(self.get_next_file(), "wb") as f:
                self._flush(f)
        else:
            with open(self.get_next_file(), "wb") as f:
                self._flush(f)

    def _flush(self, file):
        self._in_memory.clear()
        self._buffer.readinto(file)
        self._buffer.close()
        self._buffer = BytesIO()
        self._bytes_written = 0

    @property
    def extension(self):
        return ".pkl.bz2" if self.compress else ".pkl"

    def make_path_for(self, item) -> Path:
        return CACHE_DIR.joinpath(f"{self.name}_cached_{item}{self.extension}")

    def get_next_file(self) -> Path:
        existing = sorted(glob(str(self.make_path_for("*"))))
        if not existing:
            return self.make_path_for(0)

        extracted = [
            int(path.split("_cached_")[-1].split(self.extension)[0])
            for path in existing
        ]

        return self.make_path_for(max(extracted) + 1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()
