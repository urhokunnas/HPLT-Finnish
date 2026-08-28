import json

LABEL_HIERARCHY = {
    "MT": [], "LY": [], "SP": ["it"], "ID": [],
    "NA": ["ne", "sr", "nb"], "HI": ["re"],
    "IN": ["en", "ra", "dtp", "fi", "lt"],
    "OP": ["rv", "ob", "rs", "av"], "IP": ["ds", "ed"],
}

LABEL_PARENT = {c: p for p, cs in LABEL_HIERARCHY.items() for c in cs}

def return_mains(register):
    register_list = register.split("-")
    capitalised_registers = []
    for reg in register_list:
        if reg in LABEL_HIERARCHY.values(): 
            reg = LABEL_PARENT[reg]
        if reg.isupper() == True and reg not in capitalised_registers:
            capitalised_registers.append(reg)
    if len(capitalised_registers) == 1:
        main_register = capitalised_registers[0]
    elif len(capitalised_registers) == 2:
        main_register = '-'.join(sorted(capitalised_registers))
    else:
        main_register = "multi"
    return main_register

subregs = ["MT","IN-MT","IP-MT","MT-OP","ID-MT","multi","MT-NA","HI-MT","LY-MT","MT-SP"]

with open ("C:/Users/shkunn/Downloads/edu_output.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    edu_dictionary = {}
    for edu, value in file.items(): 
        edu_dictionary[edu] = {}
        for register, num in value["register"].items():
            if "MT" in register:
                r = return_mains(register)
                if r in edu_dictionary[edu].keys():
                    edu_dictionary[edu][r] += num
                else:
                    edu_dictionary[edu][r] = num

with open ("C:/Users/shkunn/Downloads/MT_finepdfs.txt", "r") as f:
    f = f.read()
    fp_dictionary = json.loads(f)

for edu, value in edu_dictionary.items():
    for sr in subregs:
        if sr not in value.keys():
            value[sr] = 0

for edu, value in fp_dictionary.items():
    for sr in subregs:
        if sr not in value.keys():
            value[sr] = 0

with open ("C:/Users/shkunn/Documents/results/MT_prop_chart.txt", "w") as f:
    f.write("Register,none,minimal,basic,moderate,high\n")
    for sr in subregs:
        f.write(f"{sr},{edu_dictionary["none"][sr]},{edu_dictionary["minimal"][sr]},{edu_dictionary["basic"][sr]},{edu_dictionary["moderate"][sr]},{edu_dictionary["high"][sr]}\n")




with open ("C:/Users/shkunn/Documents/results/MT_fp_chart.txt", "w") as f:
    f.write("Register,<0.3771,0.3771–0.8929,0.8929–1.1998,1.1998–2.6491,>2.6491")
    for sr in subregs:
        f.write(f"{sr},{fp_dictionary["0"][sr]},{fp_dictionary["1"][sr]},{fp_dictionary["2"][sr]},{fp_dictionary["3"][sr]},{fp_dictionary["4"][sr]}\n")