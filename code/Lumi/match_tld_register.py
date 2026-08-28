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

register_counter = {}
country_counter = {}

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
        propella_json = json.loads(line) 
        probs = propella_json.get("web-register", {})
        register = assign_labels (probs) #returns registers as a string
        if register in register_counter.keys():
            pass
        else:
            register_counter[register] = {"tld": {}, 
                                 "regional_relevance": {},
                                 "country_relevance": {}} #dictionary for each aspect to keep them separate
        id_num = propella_json["id"]
        tld_id = tld_json[id_num]
        tld = tld_id["tld"]
        for item in  tld_id["country_relevance"]:
            if item in register_counter[register]["country_relevance"].keys(): #adds to the register counter
                register_counter[register]["country_relevance"][item] += 1
            else:
                register_counter[register]["country_relevance"][item] = 1

            if item in country_counter.keys():                  #creating and filling the country counter
                pass
            else:
                country_counter[item] = {"register": {},
                                        "tld": {}, 
                                        "regional_relevance": {}}
            if register in country_counter[item]["register"].keys(): #adding register information to the country counter
                 country_counter[item]["register"][register] += 1
            else:
                country_counter[item]["register"][register] = 1
            if tld in country_counter[item]["tld"].keys(): #tld for the country counter
                country_counter[item]["tld"][tld] += 1
            else:
                country_counter[item]["tld"][tld] = 1
            for region in  tld_id["regional_relevance"]: #runs through regions
                if region in country_counter[item]["regional_relevance"].keys():
                    country_counter[item]["regional_relevance"][region] += 1
                else:
                    country_counter[item]["regional_relevance"][region] = 1

        if tld in register_counter[register]["tld"].keys():
            register_counter[register]["tld"][tld] += 1
        else:
            register_counter[register]["tld"][tld] = 1
        for item in  tld_id["regional_relevance"]: 
            if item in register_counter[register]["regional_relevance"].keys():
                register_counter[register]["regional_relevance"][item] += 1
            else:
                register_counter[register]["regional_relevance"][item] = 1
    propella_file.close()
    tld_file.close()
    end_process = time.time()
    print(f"Finished processing {propella_item} at time {end_process - start: .2f} seconds")

register_output_file = output_dir + "/register_output.txt"
with open (register_output_file, "w") as f:
    json.dump(register_counter, f)
country_output_file = output_dir + "/country_output.txt"
with open (country_output_file, "w") as f:
    json.dump(country_counter, f)
end = time.time()
print(f'Elapsed: {end - start:.2f} seconds')