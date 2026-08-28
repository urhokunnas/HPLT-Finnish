#code for pulling texts with a specific register into a file

import json
import sys 

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

none_list = []
minimal_list = []
basic_list = []
moderate_list = []
high_list = []

with open (sys.argv[1], "r") as f:
    for line in f:
        doc = json.loads(line)
        probs = doc.get("web-register", {})
        register = assign_labels (probs)
        if register != "OP-rs":
            continue
        edu = doc["propella-4b"]["educational_value"]
        if edu == "none":
            none_list.append(doc)
        elif edu == "minimal":
            minimal_list.append(doc)
        elif edu == "basic":
            basic_list.append(doc)
        elif edu == "moderate":
            moderate_list.append(doc)
        elif edu == "high":
            high_list.append(doc)

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/rs_edu_none.txt", "a","utf-16") as f:
    f.write(f"Number of documents: {len(none_list)}\n")
    for item in none_list:
        json.dump(item, f)
        f.write("\n\n")

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/rs_edu_minimal.txt", "a","utf-16") as f:
    f.write(f"Number of documents: {len(minimal_list)}\n")
    for item in minimal_list:
        json.dump(item, f)
        f.write("\n\n")

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/rs_edu_basic.txt","utf-16", "a") as f:
    f.write(f"Number of documents: {len(basic_list)}\n")
    for item in basic_list:
        json.dump(item, f)
        f.write("\n\n")

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/rs_edu_moderate.txt", "a", "utf-16") as f:
    f.write(f"Number of documents: {len(moderate_list)}\n")
    for item in moderate_list:
        json.dump(item, f)
        f.write("\n\n")

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/rs_edu_high.txt", "a") as f:
    f.write(f"Number of documents: {len(high_list)}\n")
    for item in high_list:
        json.dump(item, f)
        f.write("\n\n")



        
