#gets counts of how the Propella content_safety label is present in different registers and educational value categories 

import json
import os
import sys

#files with document ids, top level domains, country and region labels 
tld_dir = sys.argv[1]
#full files, include all the other metadata 
propella_dir = sys.argv[2]
#directory where output files will be put  
output_dir = sys.argv[3]
tld_filenames = os.listdir(tld_dir)
propella_filenames = os.listdir(propella_dir)
tld_list = []
propella_list = []

for item in tld_filenames:
    name = tld_dir + "/" + item
    tld_list.append(name)

tld_list.sort()

for item in propella_filenames:
    name = propella_dir + "/" + item
    propella_list.append(name)

propella_list.sort()

register_counter = {}
educational_counter = {}
safety_counter = {}

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


for tld_item, propella_item in zip(tld_list, propella_list):
    propella_file = open(propella_item, "r")
    tld_file = open(tld_item, "r")
    tld_text = tld_file.read() 
    tld_json = json.loads(tld_text)
    for line in propella_file:
        propella_json = json.loads(line) 
        probs = propella_json.get("web-register", {})
        register = assign_labels (probs) #returns registers as a string

        if register in register_counter.keys():
            pass
        else:
            register_counter[register] = {"educational_value": {}, 
                                 "content_safety": {}} #dictionary for each aspect to keep them separate
        
        educational_value = propella_json["propella-4b"]["educational_value"]
        if educational_value == "":
            educational_value = "no_label"
        content_safety = propella_json["propella-4b"]["content_safety"]
        if content_safety == "":
            content_safety = "no_label"
        if educational_value in educational_counter.keys():
            pass
        else:
            educational_counter[educational_value] = {"register": {},
                "tld": {}, "regional_relevance": {},
                "country_relevance": {}, "content_safety": {}}
        
        if content_safety in safety_counter.keys():
            pass
        else:
            safety_counter[content_safety] = {"register": {},
                "tld": {}, "regional_relevance": {},
                "country_relevance": {}, "educational_value": {}}

        id_num = propella_json["id"]
        tld_id = tld_json[id_num]
        tld = tld_id["tld"]

        if register in educational_counter[educational_value]["register"].keys():
            educational_counter[educational_value]["register"][register] += 1
        else:
            educational_counter[educational_value]["register"][register] = 1

        if register in safety_counter[content_safety]["register"].keys():
            safety_counter[content_safety]["register"][register] += 1
        else:
            safety_counter[content_safety]["register"][register] = 1

        if tld in educational_counter[educational_value]["tld"].keys():
            educational_counter[educational_value]["tld"][tld] += 1
        else:
            educational_counter[educational_value]["tld"][tld] = 1

        if tld in safety_counter[content_safety]["tld"].keys():
            safety_counter[content_safety]["tld"][tld] += 1
        else:
            safety_counter[content_safety]["tld"][tld] = 1

        for item in tld_id["country_relevance"]:
            if item in educational_counter[educational_value]["country_relevance"].keys(): 
                educational_counter[educational_value]["country_relevance"][item] += 1
            else:
                educational_counter[educational_value]["country_relevance"][item] = 1

            if item in safety_counter[content_safety]["country_relevance"].keys():
                safety_counter[content_safety]["country_relevance"][item] += 1
            else:
                safety_counter[content_safety]["country_relevance"][item] = 1
        for item in tld_id["regional_relevance"]:
            if item in educational_counter[educational_value]["regional_relevance"].keys(): 
                educational_counter[educational_value]["regional_relevance"][item] += 1
            else:
                educational_counter[educational_value]["regional_relevance"][item] = 1

            if item in safety_counter[content_safety]["regional_relevance"].keys():
                safety_counter[content_safety]["regional_relevance"][item] += 1
            else:
                safety_counter[content_safety]["regional_relevance"][item] = 1
        
        if educational_value in safety_counter[content_safety]["educational_value"].keys():
            safety_counter[content_safety]["educational_value"][educational_value] += 1
        else:
            safety_counter[content_safety]["educational_value"][educational_value] = 1

        if content_safety in educational_counter[educational_value]["content_safety"].keys():
            educational_counter[educational_value]["content_safety"][content_safety] += 1
        else:
            educational_counter[educational_value]["content_safety"][content_safety] = 1
        
        if educational_value in register_counter[register]["educational_value"].keys():
            register_counter[register]["educational_value"][educational_value] += 1
        else:
            register_counter[register]["educational_value"][educational_value] = 1
        if content_safety in register_counter[register]["content_safety"].keys():
            register_counter[register]["content_safety"][content_safety] += 1
        else:
            register_counter[register]["content_safety"][content_safety] = 1

    propella_file.close()
    tld_file.close()

register_output_file = output_dir + "/register_edu_safety.txt"
with open (register_output_file, "w") as f:
    json.dump(register_counter, f)

safety_output_file = output_dir + "/safety_output.txt"
with open (safety_output_file, "w") as f:
    json.dump(safety_counter, f)

edu_output_file = output_dir + "/edu_output.txt"
with open (edu_output_file, "w") as f:
    json.dump(educational_counter, f)


        
      