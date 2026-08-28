from glob import glob
import json

path = "/scratch/project_462001491/galicato/stripped_data"
files = glob(path+"/*.jsonl")

cats = [0.377100,0.892900,1.199800,2.649100]

# Cat 1 (Bottom 38.19%):               <= 0.377100
# Cat 2 (38.19% to 72.32% / +34.13%):    0.377100 to 0.892900
# Cat 3 (72.32% to 89.86% / +17.54%):    0.892900 to 1.199800
# Cat 4 (89.86% to 99.13% / +9.27%):     1.199800 to 2.649100
# Cat 5 (Top 0.87%):                     > 2.649100

edus = {i:{} for i in range(5)}

for i,file in enumerate(files):
    print(f"Processing file {i}")
    with open(file,'r') as f:
        for line in f:
            try:
                jdata = json.loads(line)
                fp = jdata['finepdfs-edu']
                propella = jdata['propella-4b']['educational_value']
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
                if propella not in edus[sel]:
                    edus[sel][propella] = 1
                else:
                    edus[sel][propella] += 1 
            except ValueError as e:
                print(e)

out_path1 = "/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/edu_comparison.txt"

with open (out_path1, "w") as f:
    json.dump(edus, f)