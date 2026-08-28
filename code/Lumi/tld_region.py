import json
import os
import sys
import time

start = time.time()
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

tld_counter = {}
region_counter = {}
doc_amount = 0 

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
    start_process = time.time()
    print(f"Starting to process {propella_item} at time {start_process - start: .2f} seconds")
    propella_file = open(propella_item, "r")
    tld_file = open(tld_item, "r")
    tld_text = tld_file.read() 
    tld_json = json.loads(tld_text)
    for line in propella_file:
        doc_amount += 1
        propella_json = json.loads(line) 
        probs = propella_json.get("web-register", {})
        id_num = propella_json["id"]
        tld_id = tld_json[id_num]
        tld = tld_id["tld"]
        register = assign_labels (probs) #returns registers as a string
        if tld in tld_counter.keys():
            pass
        else:
            tld_counter[tld] = {"register": {}, 
                                 "regional_relevance": {},
                                 "country_relevance": {}} #dictionary for each aspect to keep them separate
        #filling the tld counter
        if register in tld_counter[tld]["register"].keys():
            tld_counter[tld]["register"][register] += 1
        else:
            tld_counter[tld]["register"][register] = 1
        for country in tld_id["country_relevance"]:
            if country in tld_counter[tld]["country_relevance"].keys():
                tld_counter[tld]["country_relevance"][country] += 1
            else:
                tld_counter[tld]["country_relevance"][country] = 1
        for reg in tld_id["regional_relevance"]:
            if reg in tld_counter[tld]["regional_relevance"]:
                tld_counter[tld]["regional_relevance"][reg] += 1
            else:
                tld_counter[tld]["regional_relevance"][reg] = 1
        #moving to filling the region counter
            if reg in region_counter.keys():
                pass
            else:
                region_counter[reg] = {"register": {}, "tld": {}, "country_relevance": {}} #creates nested dictonary for each region

            if register in region_counter[reg]["register"].keys():
                region_counter[reg]["register"][register] += 1
            else:
                region_counter[reg]["register"][register] = 1
            if tld in region_counter[reg]["tld"].keys():
                region_counter[reg]["tld"][tld] += 1
            else:
                region_counter[reg]["tld"][tld] = 1
            for country in tld_id["country_relevance"]:
                if country in region_counter[reg]["country_relevance"].keys():
                    region_counter[reg]["country_relevance"][country] += 1
                else:
                    region_counter[reg]["country_relevance"][country] = 1
            

    propella_file.close()
    tld_file.close()
    end_process = time.time()
    print(f"Finished processing {propella_item} at time {end_process - start: .2f} seconds")

tld_output_file = output_dir + "/tld_output.txt"
with open (tld_output_file, "w") as f:
    json.dump(tld_counter, f)
region_output_file = output_dir + "/region_output.txt"
with open (region_output_file, "w") as f:
    json.dump(region_counter, f)
end = time.time()
print(f'Elapsed: {end - start:.2f} seconds')
print(f"Total size: {doc_amount}")