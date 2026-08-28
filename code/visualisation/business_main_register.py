import json
import numpy as np
import pandas as pd
import plotly.express as px

business_counter = {}

def return_main(register):
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
    return main_register

with open ("C:/Users/shkunn/Documents/results/sorted/business_sorted.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    for sector, content in file.items():
        if sector not in business_counter.keys():
            business_counter[sector] = {}
        for register, value in content["register"].items():
            main_register = return_main(register)
            if main_register in business_counter[sector].keys(): 
                business_counter[sector][main_register] += value[0]
            else:
                business_counter[sector][main_register] = value[0]

row_counter = 0
dict_for_df = {}

for sector, content in business_counter.items():
    total = sum(content.values())
    for register, value in content.items():
        dict_for_df[row_counter] = [sector, register, (value/total) *100]
        row_counter += 1 

df = pd.DataFrame.from_dict(dict_for_df, orient="index", columns=["business_sector","main_register","percent"])

print(df)
bar = px.bar(df,x="business_sector",y="percent",color="main_register",barmode="stack")

bar.update_layout(legend_title_text='Main register', 
        title_text="Distribution of main registers between business sectors",
                      yaxis_title_text="Percent", xaxis_title_text="Business sector")

bar.show()