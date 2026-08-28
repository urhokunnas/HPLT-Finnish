import json 
import numpy as np
import pandas as pd 
import scipy.stats as st

edus = []
businesses = []
sums = []
with open ("C:/Users/shkunn/Downloads/business_sector.txt", "r") as f:
    file = f.read()
    business_dict = json.loads(file)
    for sector, content in business_dict.items():
        for edu, sum in content["educational_value"].items():
            edus.append(edu)
            businesses.append(sector)
            sums.append(sum)
        
bus_dict = {}
for e, b, s in zip(edus, businesses, sums):
    if b in bus_dict.keys():
        bus_dict[b][e] = s
    else:
        bus_dict[b] = {e: s}

scores = ["none","minimal","basic","moderate","high"]

for b, value in bus_dict.items():
    for s in scores:
        if s not in value.keys():
            bus_dict[b][s] = "0"

with open ("C:/Users/shkunn/Documents/results/propella_business_chart.txt", "w") as f:
    f.write("business,none,minimal,basic,moderate,high\n")
    for key, value in bus_dict.items():
        f.write(f"{key},{value["none"]},{value["minimal"]},{value["basic"]},{value["moderate"]},{value["high"]}\n")


