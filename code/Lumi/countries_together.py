import json
import os
import sys

country_counter = {}
#files with document ids, top level domains, country and region labels 
tld_dir = sys.argv[1]
#full files, include all the other metadata 
propella_dir = sys.argv[2]
#directory where output files will be put  
output_dir = sys.argv[3]
tld_filenames = os.listdir(tld_dir)
propella_filenames = os.listdir(propella_dir)
tld_filenames = os.listdir(tld_dir)
propella_list = []
tld_list = []
for item in propella_filenames:
    name = propella_dir + "/" + item
    propella_list.append(name)
propella_list.sort()
for item in tld_filenames:
    name = tld_dir + "/" + item
    tld_list.append(name)
tld_list.sort()

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
        id_num = propella_json["id"]
        tld_id = tld_json[id_num]
        tld = tld_id["tld"]
        register = assign_labels (probs) #returns registers as a string
        countries = tld_id["country_relevance"]
        country = "-".join(set(sorted(countries))) #combines countries so that texts relating to combinations of countries can be considered
        regions = tld_id["regional_relevance"]
        region = "-".join(set(sorted(regions)))
        if country in country_counter.keys():
            pass
        else: 
            country_counter[country] = {"tld": {}, "regional_relevance": {}, "register": {}}
        if tld in country_counter[country]["tld"].keys():
            country_counter[country]["tld"][tld] += 1
        else:
            country_counter[country]["tld"][tld] = 1
        if register in country_counter[country]["register"].keys():
            country_counter[country]["register"][register] += 1
        else:
            country_counter[country]["register"][register] = 1
        if region in country_counter[country]["regional_relevance"].keys():
            country_counter[country]["regional_relevance"][region] += 1
        else:
            country_counter[country]["regional_relevance"][region] = 1
    propella_file.close()
    tld_file.close()

output_file = output_dir + "/countries_together_output.txt"
with open (output_file, "w") as f:
    json.dump(country_counter, f)

