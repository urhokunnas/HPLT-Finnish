import json
import numpy as np
import pandas as pd
import plotly.express as px

edu_totals = {"none":19642994, "minimal":17556194, "basic": 9022275, "moderate": 4768090, "high": 446010 }
#total size of each educational category

targeted_register = "OP"

def get_main_register(register):
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
    return(main_register)


with open ("C:/Users/shkunn/Downloads/edu_output.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    edu_dictionary = {}
    for edu, value in file.items(): 
        edu_dictionary[edu] = {}
        for register, sum in value["register"].items():
            if get_main_register(register) == targeted_register:
                edu_dictionary[edu][register] = sum


edu_props = {}
for edu, value in edu_dictionary.items():
    edu_props[edu] = {}
    for register, sum in value.items():
        edu_props[edu][register] = sum
#get charts like this for all registers then do the same but with equalised bars so it's easier to compare changes in proportion 
#between educational categories 
row_counter = 0
dict_for_df = {}
dict_even = {}

for edu, value in edu_props.items():
    total = 0
    for item in value.values():
        total += item
    for register, sum in value.items():
        dict_for_df[row_counter] = [edu, register, sum / edu_totals[edu]]
        dict_even[row_counter] = [edu, register, sum/total]
        row_counter += 1

#turn into percentages 

df = pd.DataFrame.from_dict(dict_for_df, orient="index", columns=["edu","register","proportion"])
even_df = pd.DataFrame.from_dict(dict_even, orient="index",columns=["edu","register","percent"])

prop_bar = px.bar(df,x="edu", y="proportion",color="register",barmode="stack")

prop_bar.update_layout(legend_title_text='Register', 
        title_text=f"Distribution of texts in register {targeted_register} (as fraction of all texts in the category)",
                      xaxis_title_text="Count", yaxis_title_text="Educational category")

even_bar = px.bar(even_df,x="edu",y="percent",color="register",barmode="stack")

even_bar.update_layout(legend_title_text='Register', 
        title_text=f"Distribution of texts in register {targeted_register}",
                      xaxis_title_text="Count", yaxis_title_text="Educational category")
prop_bar.show()
even_bar.show()