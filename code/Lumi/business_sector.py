#gathers details for how many documents are in each business category and what registers, TLDs and other details they have

import json
import os
import sys

#files with document ids, top level domains, country and region labels 
tld_dir = sys.argv[1]
#full files, include all the other metadata 
propella_dir = sys.argv[2]

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

business_counter = {}

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
        id_num = propella_json["id"]
        tld_id = tld_json[id_num]
        tld = tld_id["tld"]
        safety = propella_json["propella-4b"]["content_safety"]
        countries = propella_json["propella-4b"]["country_relevance"]
        regions = propella_json["propella-4b"]["regional_relevance"]
        for business in propella_json["propella-4b"]["business_sector"]:
            if business in business_counter.keys():
                pass
            else:
                business_counter[business] = {"tld": {},
                                              "register": {},
                                              "country_relevance": {}, 
                                              "regional_relevance": {},
                                              "content_safety": {}}
            if tld in business_counter[business]["tld"].keys():
                business_counter[business]["tld"][tld] += 1
            else:
                business_counter[business]["tld"][tld] = 1
            if safety in business_counter[business]["content_safety"].keys():
                business_counter[business]["content_safety"][safety] += 1
            else:
                business_counter[business]["content_safety"][safety] = 1
            if register in business_counter[business]["register"].keys():
                business_counter[business]["register"][register] += 1
            else:
                business_counter[business]["register"][register] = 1
            for country in countries:
                if country in business_counter[business]["country_relevance"].keys():
                    business_counter[business]["country_relevance"][country] += 1
                else:
                    business_counter[business]["country_relevance"][country] = 1
            for region in regions:
                if region in business_counter[business]["regional_relevance"].keys():
                    business_counter[business]["regional_relevance"][region] += 1
                else:
                    business_counter[business]["regional_relevance"][region] = 1

    propella_file.close()
    tld_file.close()

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/business_sector.txt", "w") as f:
    json.dump(business_counter, f)

            

            