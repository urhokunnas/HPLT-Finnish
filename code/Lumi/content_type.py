#gather propella content_type and see how it relates to register and edu

import json
import os 
import sys

#directory containing unzipped full files
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

type_counter = {}
row_counter = 0

for doc in propella_list:
    file = open(doc, "r")
    for line in file:
        f = json.loads(line)
        probs = f.get("web-register", {})
        register = assign_labels (probs)
        edu = f["propella-4b"]["educational_value"]
        content_type = f["propella-4b"]["content_type"]
        business_sector = f["propella-4b"]["business_sector"]
        type_counter[row_counter] = [edu, content_type, register, business_sector] 
        row_counter += 1 

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/content_type.txt", "w") as f:
    json.dump(type_counter, f)

