import json
import os 
import sys

#files to be processed
propella_dir = sys.argv[1]

propella_filenames = os.listdir(propella_dir)
propella_list = []

for item in propella_filenames:
    name = propella_dir + "/" + item
    propella_list.append(name)

quality_counter = {}

REGISTERS = ["dtp", "HI", "HI-IN", "ID", "IN", "IP", "MT", "NA", "ne", "OP", "SP", "LY", "no-label"]

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

# pull content quality vs edu and register 

for f in propella_list: 
    file = open(f)
    for line in file:
        j = json.loads(line)
        probs = j.get("web-register", {})
        register = assign_labels (probs) #returns registers as a string
        edu = j["propella-4b"]["educational_value"]
        quality = j["propella-4b"]["content_quality"]
        type = j["propella-4b"]["content_type"]

        if quality not in quality_counter.keys():
            quality_counter[quality] = {"edu": {}, "type": {}, "register": {}}
        for item, name in [[edu, "edu"], [register, "register"]]:
            if item in quality_counter[quality][name].keys():
                quality_counter[quality][name][item] += 1
            else:
                quality_counter[quality][name][item] = 1
        for t in type:
            if t in quality_counter[quality]["type"].keys():
                quality_counter[quality]["type"][t] += 1
            else:
                quality_counter[quality]["type"][t] = 1 

    file.close()

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/quality.txt", "w") as f:
    json.dump(quality_counter, f)

    