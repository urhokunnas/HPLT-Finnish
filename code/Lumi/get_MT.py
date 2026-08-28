import json 
import sys

def return_mains(register):
    register_list = register.split("-")
    capitalised_registers = []
    for reg in register_list:
        if reg.isupper() == True:
            capitalised_registers.append(reg)
    if len(capitalised_registers) == 1:
        main_register = capitalised_registers[0]
    elif len(capitalised_registers) == 2:
        main_register = '-'.join(sorted(capitalised_registers))
    else:
        main_register = "multi"
    return main_register

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

HI_texts = {}
IN_texts = {}

with open (sys.argv[1], "r") as f:
    for line in f:
        doc = json.loads(line)
        fp = doc["finepdfs-edu"]
        if fp < 2.649100:
            continue
        probs = doc.get("web-register", {})
        register = assign_labels (probs)
        main_register = return_mains(register)
        if main_register == "IN-MT":
            IN_texts[doc["id"]] = [fp, doc["propella-4b"]["one_sentence_description"], doc["text"]]
        elif main_register == "HI-MT":
            HI_texts[doc["id"]] = [fp, doc["propella-4b"]["one_sentence_description"], doc["text"]]
        else:
            continue 

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/IN_MT_high.txt", "a") as f:
    json.dump(IN_texts, f)

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/HI_MT_high.txt", "a") as f:
    json.dump(HI_texts, f)