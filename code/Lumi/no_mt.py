# get data without any texts with MT in the register 
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

tld_counter = {}
region_counter = {}
register_counter = {}
country_counter = {}

mt_counter = 0

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
        if "MT" in register:
            mt_counter += 1 #ignore documents with the register MT or MT hybrids and count the amount
            continue 
        if tld in tld_counter.keys():
            pass
        else:
            tld_counter[tld] = {"register": {}, 
                                 "regional_relevance": {},
                                 "country_relevance": {}} #dictionary for each aspect to keep them nice and separate
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
        #register counter
        if register in register_counter.keys():
            pass
        else:
            register_counter[register] = {"tld": {}, 
                                 "regional_relevance": {},
                                 "country_relevance": {}}
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
        for item in  tld_id["regional_relevance"]: #should run through everything in the list and add to their frequency data
            if item in register_counter[register]["regional_relevance"].keys():
                register_counter[register]["regional_relevance"][item] += 1
            else:
                register_counter[register]["regional_relevance"][item] = 1

    propella_file.close()
    tld_file.close()
print(f"Amount of documents with machine translated content: {mt_counter}")

tld_output_file = output_dir + "/tld_output_noMT.txt"
with open (tld_output_file, "w") as f:
    json.dump(tld_counter, f)
region_output_file = output_dir + "/region_output_noMT.txt"
with open (region_output_file, "w") as f:
    json.dump(region_counter, f)
country_output_file = output_dir + "/country_output_noMT.txt"
with open (country_output_file, "w") as f:
    json.dump(country_counter, f)
register_output_file = output_dir + "/register_output_noMT.txt"
with open (register_output_file, "w") as f:
    json.dump(register_counter, f)
