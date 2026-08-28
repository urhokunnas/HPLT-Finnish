import json
import os
import sys

#files to be processed
tld_dir = sys.argv[1]
propella_dir = sys.argv[2]
#directory where output files will be put  
output_dir = sys.argv[3]
#gives the names of the files (like 10_1.jsonl)
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

pure_counter = {} #texts where the main register is OP
hybrid_counter = {} #hybrids of multiple main registers, one of them OP 


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

def return_main(register):
    register_list = register.split("-")
    if len(register_list) == 1:
        main_register = register_list[0] #if the register has only one component, that is the same as the main register
    else:
        capitalised_registers = []
        for reg in register_list:
            if reg.isupper() == True:
                capitalised_registers.append(reg)
            if len(capitalised_registers) == 1:
                main_register = capitalised_registers[0]
            else:
                main_register = "Hybrid"
    return main_register

for tld_item, propella_item in zip(tld_list, propella_list):
    propella_file = open(propella_item, "r")
    tld_file = open(tld_item, "r")
    tld_text = tld_file.read() 
    tld_json = json.loads(tld_text)
    for line in propella_file:
        propella_json = json.loads(line) 
        probs = propella_json.get("web-register", {})
        register = assign_labels (probs)
        if "OP" not in register: #only interested in documents that have something opinionated
            continue
        main_register = return_main(register)
        id_num = propella_json["id"]
        tld_id = tld_json[id_num]
        edu = propella_json["propella-4b"]["educational_value"]
        if main_register == "OP":
            if edu in pure_counter.keys():
                pass
            else:
                pure_counter[edu] = {"register": {}, 
                                 "regional_relevance": {},
                                 "country_relevance": {},
                                 "tld": {}, 
                                 "business_sector":{}}
            if register in pure_counter[edu]["register"].keys():
                pure_counter[edu]["register"][register] += 1
            else:
                pure_counter[edu]["register"][register] = 1
            if tld_id["tld"] in pure_counter[edu]["register"].keys():
                pure_counter[edu]["tld"][tld_id["tld"]] += 1
            else:
                pure_counter[edu]["tld"][tld_id["tld"]] = 1
            for item in ["regional_relevance","country_relevance","business_sector"]:
                for i in propella_json["propella-4b"][item]: 
                    if i in pure_counter[edu][item].keys():
                        pure_counter[edu][item][i] += 1
                    else:
                        pure_counter[edu][item][i] = 1
        if main_register == "Hybrid":
            if edu in hybrid_counter.keys():
                pass
            else:
                hybrid_counter[edu] = {"register": {}, 
                                 "regional_relevance": {},
                                 "country_relevance": {},
                                 "tld": {}, 
                                 "business_sector":{}}
            if register in hybrid_counter[edu]["register"].keys():
                hybrid_counter[edu]["register"][register] += 1
            else:
                hybrid_counter[edu]["register"][register] = 1
            if tld_id["tld"] in hybrid_counter[edu]["register"].keys():
                hybrid_counter[edu]["tld"][tld_id["tld"]] += 1
            else:
                hybrid_counter[edu]["tld"][tld_id["tld"]] = 1
            for item in ["regional_relevance","country_relevance","business_sector"]:
                for i in propella_json["propella-4b"][item]: 
                    if i in hybrid_counter[edu][item].keys():
                        hybrid_counter[edu][item][i] += 1
                    else:
                        hybrid_counter[edu][item][i] = 1
    propella_file.close()
    tld_file.close()

pure_output = output_dir + "/pure_OP.txt"
with open (pure_output, "w") as f:
    json.dump(pure_counter, f)

hybrid_output = output_dir + "/hybrid_OP.txt"
with open (hybrid_output, "w") as f:
    json.dump(hybrid_counter, f)
        