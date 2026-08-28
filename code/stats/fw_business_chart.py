import json 
import numpy as np
import pandas as pd 
import scipy.stats as st

edus = []
businesses = []
sums = []
with open ("C:/Users/shkunn/Downloads/finewebs_edu.txt", "r") as f:
    file = f.read()
    j = json.loads(file)
    for edu, value in j.items():
        if edu != "4" and edu != "5":
            dict = {}
            for business, num in value["business"].items():
                if business in dict.keys():
                    dict[business] += num
                else:
                    dict[business] = num
            for r, n in dict.items():
                edus.append(edu)
                businesses.append(r)
                sums.append(n)
            continue
        if edu == "4":
            dict_four_five = {}
            for business, num in value["business"].items():
                if business in dict_four_five.keys():
                    dict_four_five[business] += num
                else:
                    dict_four_five[business] = num
        if edu == "5":
            for business, num in value["business"].items():
                if business in dict_four_five.keys():
                    dict_four_five[business] += num
                else:
                    dict_four_five[business] = num

for r, n in dict_four_five.items():
    edus.append("4")
    businesses.append(r)
    sums.append(n)
        
bus_dict = {}
for e, b, s in zip(edus, businesses, sums):
    if b in bus_dict.keys():
        bus_dict[b][e] = s
    else:
        bus_dict[b] = {e: s}

scores = ["-0","0","1","2","3","4"]

for b, value in bus_dict.items():
    for s in scores:
        if s not in value.keys():
            bus_dict[b][s] = "0"

with open ("C:/Users/shkunn/Documents/results/fw_business_chart.txt", "w") as f:
    f.write("business,-1–0,0–1,1–2,2–3,3–4,4–5\n")
    for key, value in bus_dict.items():
        f.write(f"{key},{value["-0"]},{value["0"]},{value["1"]},{value["2"]},{value["3"]},{value["4"]}\n")


