import json
import numpy as np
import pandas as pd
import plotly.express as px

edu_totals = {"none":19642994, "minimal":17556194, "basic": 9022275, "moderate": 4768090, "high": 446010 }
#total size of each educational category

register_names = {"MT": "Machine translated or generated", "LY-MT":"Lyrical",
                  "MT-SP": "Spoken", "ID-MT": "Interactive discussion", "MT-NA": "Narrative",
                  "HI-MT": "How-to or instructions", "IN-MT": "Informational description", 
                  "MT-OP": "Opinion", "IP-MT": "Informational persuasion", "multi": "Three or more registers"}


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

with open ("C:/Users/shkunn/Downloads/edu_output.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    edu_dictionary = {}
    for edu, value in file.items(): 
        edu_dictionary[edu] = {}
        for register, sum in value["register"].items():
            if "MT" in register:
                reg = return_mains(register)
                if reg in edu_dictionary[edu].keys():
                    edu_dictionary[edu][reg] += sum
                else:
                    edu_dictionary[edu][reg] = sum


edu_props = {}
for edu, value in edu_dictionary.items():
    edu_props[edu] = {}
    for register, sum in value.items():
        edu_props[edu][register] = sum / edu_totals[edu]
#get charts like this for all registers then do the same but with equalised bars so it's easier to compare changes in proportion 
#between educational categories 
row_counter = 0
dict_for_df = {}
for edu, value in edu_props.items():
    for register, sum in value.items():
        if register == "MT":
            type = "MT"
        else:
            type = "Hybrid"
        register_name = register_names[register]
        percent = sum * 100
        dict_for_df[row_counter] = [edu, register, percent,type]
        row_counter += 1

df = pd.DataFrame.from_dict(dict_for_df, orient="index", columns=["edu","register","%", "type"])

bar_fig = px.bar(df, x="edu",y="%", color="register", barmode="stack",facet_row="type", text_auto='.4f')

bar_fig.update_layout(legend_title_text='Register',
                      xaxis_title_text="Educational category", 
                      font_size=18)


bar_fig.update_traces(textposition='inside')
bar_fig.update_layout(uniformtext_minsize=7, uniformtext_mode='hide',
                      yaxis = dict(tickmode = "linear", tick0 = 0, dtick = 1, ticklabelstep=2))

bar_fig.show()