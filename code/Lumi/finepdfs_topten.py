import json 
import os
import sys
import heapq

propella_dir = sys.argv[1]

propella_filenames = os.listdir(propella_dir)
propella_list = []
for item in propella_filenames:
    name = propella_dir + "/" + item
    propella_list.append(name)

finepdfs_full = []

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

for f in propella_list:
    file = open(f)
    for line in file:
        j = json.loads(line)
        probs = j.get("web-register", {})
        register = assign_labels(probs)
        propella_edu = j["propella-4b"]["educational_value"]
        finepdfs_edu = j["finepdfs-edu"]
        businesses = j["propella-4b"]["business_sector"]
        finepdfs_full.append([finepdfs_edu, register, businesses, propella_edu])

finepdfs_selected = heapq.nlargest(5143556, finepdfs_full, key=lambda x: x[0])

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/finepdfs_topten.txt", "w") as f:
    f.write(finepdfs_selected)