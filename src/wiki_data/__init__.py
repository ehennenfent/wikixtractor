import glob
from bz2 import BZ2File
import pickle
from pathlib import Path
import time
import threading

directory = Path(__file__).parent

id_to_label = {"Q": {}, "P": {}}
views = {}

with open(directory.joinpath("id_to_label.pkl"), "rb") as pkf:
    id_to_label = pickle.load(pkf)

# with open(directory.joinpath("pageviews_extracted", "pageviews_en_wikipedia.pkl"), "rb") as pkf:
#     views = pickle.load(pkf)
