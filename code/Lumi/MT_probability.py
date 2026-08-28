#see if MT probability changes as years go on 
import json
import os 
import sys

#directory with full decompressed files
propella_dir = sys.argv[1]

propella_filenames = os.listdir(propella_dir)

propella_list = []

for item in propella_filenames:
    name = propella_dir + "/" + item
    propella_list.append(name)

LABEL_HIERARCHY = {
    "MT": [], "LY": [], "SP": ["it"], "ID": [],
    "NA": ["ne", "sr", "nb"], "HI": ["re"],
    "IN": ["en", "ra", "dtp", "fi", "lt"],
    "OP": ["rv", "ob", "rs", "av"], "IP": ["ds", "ed"],
}
LABEL_PARENT = {c: p for p, cs in LABEL_HIERARCHY.items() for c in cs}

def assign_labels(probabilities): 
    labels = set()
    for label, prob in probabilities.items():
        if prob >= 0.4: #threshold for Finnish
            labels.add(label)
            if label in LABEL_PARENT: 
                labels.add(LABEL_PARENT[label]) #if text belongs to a subregister adds also the main register 
    if len(labels) == 0:
        labels.add("no-label")
    register = '-'.join(sorted(labels)) #alphabetically sorts the registers and turns them into a string 
    return register

year_counter = {}

for doc in propella_list:
    file = open(doc, "r")
    for line in file:
        f = json.loads(line)
        mt_prob = f["web-register"]["MT"]
        probs = f.get("web-register", {})
        register = assign_labels (probs)
        crawl = f["crawl_id"]
        if "CC" not in crawl:
            continue 
        year = crawl.split("-")[2]
        if year in year_counter.keys():
            year_counter[year].append([register, mt_prob])
        else:
            year_counter[year] = [[register, mt_prob]]

#for each year creates a list where every document is an item

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/MT_probability.txt", "w") as f:
    json.dump(year_counter, f)