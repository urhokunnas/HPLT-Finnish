import json
import numpy as np
import pandas as pd
import plotly.express as px

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

full_counts = {}
with open ("C:/Users/shkunn/Documents/HPLT4_Finnish/counts/edu_output.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    edu_dictionary = {}
    for edu, value in file.items(): 
        edu_dictionary[edu] = {}
        full_counts[edu] = sum(value["register"].values())
        for register, num in value["register"].items():
            if "MT" in register:
                reg = return_mains(register)
               # if reg == "MT":
                    #continue
                if reg in edu_dictionary[edu].keys():
                    edu_dictionary[edu][reg] += num
                else:
                    edu_dictionary[edu][reg] = num

with open ("C:/Users/shkunn/Documents/HPLT4_Finnish/counts/finepdfs_edu_output.txt", "r") as f:
    f = f.read()
    file = json.loads(f)
    fw_dictionary = {"-0":{},"0":{},"1":{},"2":{},"3":{},"4":{}}
    
    for edu, value in file.items():
        full_counts[edu] = sum(value["register"].values())
        for register, num in value["register"].items():
            if "MT" in register:
                reg = return_mains(register)
                #if reg == "MT":
                    #continue
                if reg in fw_dictionary[edu].keys():
                    fw_dictionary[edu][reg] += num
                else:
                    fw_dictionary[edu][reg] = num


full_counts["4"] += full_counts ["5"]
prop_dict_df = {}
fw_dict_df = {}
row_counter = 0

for edu, value in edu_dictionary.items():
    for register, sum in value.items():
        prop = sum / full_counts[edu]
        percent = prop * 100
        prop_dict_df[row_counter] = [edu, register, percent]
        row_counter += 1


fw_names = {"-0":"-1–0","0":"0–1","1":"1–2","2":"2–3","3":"3–4","4":"4–5"}
for edu, value in fw_dictionary.items():
    for register, sum in value.items():
        prop = sum / full_counts[edu]
        percent = prop *100 
        fw_dict_df[row_counter] = [fw_names[edu], register, percent]
        row_counter += 1

prop_df = pd.DataFrame.from_dict(prop_dict_df, orient="index", columns=["edu","register","%"])
fw_df = pd.DataFrame.from_dict(fw_dict_df, orient="index",columns=["edu", "register", "%"])

coloring = {"IP-MT": px.colors.qualitative.Plotly[0],
            "IN-MT": px.colors.qualitative.Plotly[1],
             "HI-MT": px.colors.qualitative.Plotly[2],
              "MT-OP": px.colors.qualitative.Plotly[3],
               "MT-NA": px.colors.qualitative.Plotly[4],
                "ID-MT": px.colors.qualitative.Plotly[5],
                 "MT-SP": px.colors.qualitative.Plotly[6],
                  "LY-MT": px.colors.qualitative.Plotly[7],
                   "multi":px.colors.qualitative.Plotly[8] }

prop_fig = px.bar(prop_df, x="edu",y="%", color="register", barmode="stack", text_auto='.2f',
                  color_discrete_map=coloring)

fw_fig = px.bar(fw_df, x="edu",y="%", color="register", barmode="stack", text_auto='.2f',
                color_discrete_map=coloring)

prop_fig.update_layout(legend_title_text='Register',
                      xaxis_title_text="Educational category", 
                      font_size=18,
                       yaxis = dict(tickmode = "linear", tick0 = 0, dtick = 0.1, ticklabelstep=5))
fw_fig.update_layout(legend_title_text='Register',
                      xaxis_title_text="Education score", 
                      font_size=18,  
                      yaxis = dict(tickmode = "linear", tick0 = 0, dtick = 0.1, ticklabelstep=5),)

prop_fig.show()
fw_fig.show()