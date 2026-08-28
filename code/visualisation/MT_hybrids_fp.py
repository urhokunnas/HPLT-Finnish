import json
import numpy as np
import pandas as pd
import plotly.express as px

prop_check = {"MT":0,"IN-MT":0,"IP-MT":0,"MT-OP":0,"ID-MT":0,"multi":0,"MT-NA":0,"HI-MT":0,"LY-MT":0,"MT-SP":0}
fp_check = {"MT":0,"IN-MT":0,"IP-MT":0,"MT-OP":0,"ID-MT":0,"multi":0,"MT-NA":0,"HI-MT":0,"LY-MT":0,"MT-SP":0}
edu_totals = {"none":19642994, "minimal":17556194, "basic": 9022275, "moderate": 4768090, "high": 446010 }
#total size of each educational category

data = {"0": {"IP": 7553618, "NA": 5203261, "Hybrid": 2603863, "IN": 1219847, "OP": 571102, "HI": 241807, "MT": 1007799, "ID": 1224856, "SP": 11543, "LY": 7524}, "1": {"NA": 6103846, "OP": 746534, "ID": 1998253, "IP": 3061920, "HI": 454244, "IN": 1462561, "Hybrid": 2660989, "MT": 1012873, "SP": 35957, "LY": 17986}, "2": {"Hybrid": 1642949, "NA": 2951458, "IP": 1277866, "OP": 527997, "IN": 1198847, "MT": 457041, "HI": 336531, "ID": 588351, "SP": 29446, "LY": 9677}, "3": {"NA": 1401056, "IP": 581463, "Hybrid": 986372, "IN": 922071, "OP": 270746, "HI": 227065, "MT": 178287, "SP": 14033, "ID": 183374, "LY": 3127}, "4": {"IN": 159048, "NA": 63725, "Hybrid": 121060, "IP": 37724, "MT": 11508, "OP": 15984, "HI": 31904, "ID": 5511, "SP": 892, "LY": 67}}

fp_totals = {}
for n in ["0","1","2","3","4"]:
    total = sum(data[n].values())
    fp_totals[n] = total

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

prop_sum = 0
fp_sum = 0

with open ("C:/Users/shkunn/Downloads/edu_output.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    edu_dictionary = {}
    for edu, value in file.items(): 
        edu_dictionary[edu] = {}
        for register, num in value["register"].items():
            if "MT" in register:
                r = return_mains(register)
                prop_sum += num
                if r in edu_dictionary[edu].keys():
                    edu_dictionary[edu][r] += num
                else:
                    edu_dictionary[edu][r] = num

with open ("C:/Users/shkunn/Downloads/MT_finepdfs.txt", "r") as f:
    f = f.read()
    fp_dictionary = json.loads(f)

edu_props = {}
for edu, value in edu_dictionary.items():
    edu_props[edu] = {}
    for register, num in value.items():
        prop_check[register] += num
        edu_props[edu][register] = num / edu_totals[edu]

for edu, value in fp_dictionary.items():
    edu_props[edu] = {}
    for register, num in value.items():
        fp_sum += num
        fp_check[register] += num
        edu_props[edu][register] = num /fp_totals[edu]

row_counter = 0 
dict_for_df = {}

conversion = {"none":"0","minimal":"1","basic":"2","moderate":"3","high":"4"}
for edu, value in edu_props.items():
    if edu in conversion.keys():
        e = conversion[edu]
        source = "Propella"
    else:
        e = edu
        source = "FinePDFs"
    for register, num in value.items():
        if register =="MT":
            continue
            type = "MT"
        else:
            type = "Hybrid"
        percent = num * 100 
        dict_for_df[row_counter] = [e, register, percent, type, source]
        row_counter += 1

df = pd.DataFrame.from_dict(dict_for_df, orient="index", columns=["edu","register","%","type","source"])

coloring = {"IP-MT": px.colors.qualitative.Plotly[0],
            "MT-NA": px.colors.qualitative.Plotly[1],
             "IN-MT": px.colors.qualitative.Plotly[2],
              "HI-MT": px.colors.qualitative.Plotly[3],
               "ID-MT": px.colors.qualitative.Plotly[4],
                "MT": px.colors.qualitative.Plotly[5],
                 "LY-MT": px.colors.qualitative.Plotly[6],
                  "MT-SP": px.colors.qualitative.Plotly[7],
                   "MT-OP":px.colors.qualitative.Plotly[8],
                    "multi":px.colors.qualitative.Plotly[9] }

fig = px.bar(df,x="edu",y="%",color="register",barmode="stack",facet_row="source", color_discrete_map=coloring,
            facet_row_spacing=0.12)

fig.update_layout(xaxis_title_text="Educational category", 
                    font_size=24, height=800,
                    legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="left"),legend_title_side = "top center",
                                           legend_title_text="Register")

fig.for_each_annotation(lambda a: a.update(text=""))

fig.update_layout({'yaxis': dict(matches=None,tickmode = "linear", tick0 = 0, dtick = 0.2, ticklabelstep=5)})
fig.update_layout({'yaxis2': dict(matches=None,tickmode = "linear", tick0 = 0, dtick = 0.2, ticklabelstep=5)})

fig.show()
