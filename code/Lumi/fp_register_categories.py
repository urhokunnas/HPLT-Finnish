from glob import glob
import numpy as np
import json

path = "/scratch/project_462001491/galicato/stripped_data"
files = glob(path+"/*.jsonl")

cats = [0.377100,0.892900,1.199800,2.649100]

# Cat 1 (Bottom 38.19%):               <= 0.377100
# Cat 2 (38.19% to 72.32% / +34.13%):    0.377100 to 0.892900
# Cat 3 (72.32% to 89.86% / +17.54%):    0.892900 to 1.199800
# Cat 4 (89.86% to 99.13% / +9.27%):     1.199800 to 2.649100
# Cat 5 (Top 0.87%):                     > 2.649100

def return_main(register_list):
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

main_registers = {i:{} for i in range(5)}
registers = {i:{} for i in range(5)}

count_all = 0
counts = {i:0 for i in range(5)}

for i,file in enumerate(files):
    print(f"Processing file {i}")
    with open(file,'r') as f:
        for line in f:
            try:
                jdata = json.loads(line)
                fp = jdata['finepdfs-edu']
                register_list = jdata['assigned_labels']
                if "MT" not in register_list:
                    continue
                main_register = return_main(register_list)
                count_all += 1
                if float(fp) <= cats[0]:
                    sel = 0
                elif float(fp) <= cats[1]:
                    sel = 1
                elif float(fp) <= cats[2]:
                    sel = 2
                elif float(fp) <= cats[3]:
                    sel = 3
                else:
                    sel = 4
                counts[sel] +=1
                if main_register not in main_registers[sel]:
                    main_registers[sel][main_register] = 1
                else:
                    main_registers[sel][main_register] += 1
            except ValueError as e:
                print(e)
                
out_path1 = "/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/MT_finepdfs.txt"

print(counts)
with open (out_path1, "w") as f:
    json.dump(main_registers, f)

