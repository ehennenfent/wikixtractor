from bz2 import BZ2File
import json
import pickle

pairs = []
mapping = {}

with BZ2File("properties.json.bz2") as f:
    for line in f:
        data = json.loads(line.strip().strip(b","))
        id = data["id"]

        labels = data["labels"]
        if "en" in labels:
            # print(id.ljust(5), "::", labels["en"]["value"])
            pairs.append((int(id[1:]), labels["en"]["value"]))

for id, val in sorted(pairs, key = lambda x: x[0]):
    fmt = f"P{id}"
    print(fmt.ljust(5), "-->", val)
    
    if fmt in mapping:
        print("Duplicate ID:", fmt)
    mapping[fmt] = val

with open("properties.pkl", "wb") as pickf:
    pickle.dump(mapping, pickf)