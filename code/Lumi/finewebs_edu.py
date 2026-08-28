import json
import os 
import sys

propella_dir = sys.argv[1]

propella_filenames = os.listdir(propella_dir)
propella_list = []
for item in propella_filenames:
    name = propella_dir + "/" + item
    propella_list.append(name)

fineweb_counter = {}

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
        fineweb_edu = j["finepdfs-edu"]
        businesses = j["propella-4b"]["business_sector"]
        quality = j["propella-4b"]["content_quality"]

        fine_str = str(fineweb_edu)
        fine_list = fine_str.split(".")
        fineweb_simple = fine_list[0] #one of 0, 1, 2, 3, 4 

        if fineweb_simple not in fineweb_counter.keys():
            fineweb_counter[fineweb_simple] = {"prop_edu":{},"register":{},
                                               "business":{},"quality":{}}
        for item, name in [[propella_edu,"prop_edu"], [register, "register"],[quality, "quality"]]:
            if item in fineweb_counter[fineweb_simple][name].keys():
                fineweb_counter[fineweb_simple][name][item] += 1
            else:
                fineweb_counter[fineweb_simple][name][item] = 1
        for b in businesses:
            if b in fineweb_counter[fineweb_simple]["business"].keys():
                fineweb_counter[fineweb_simple]["business"][b] += 1
            else:
                fineweb_counter[fineweb_simple]["business"][b] = 1
    file.close()

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/finewebs_edu.txt", "w") as f:
    json.dump(fineweb_counter, f)

