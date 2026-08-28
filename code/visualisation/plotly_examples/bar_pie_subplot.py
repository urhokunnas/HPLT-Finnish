import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
    #almost everything else can and should be done with plotly.express, but it doesn't support subplots 
    #so we need plotly.graph_objects and plotly.subplots


with open ("C:/Users/shkunn/Downloads/edu_output.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    edu_dictionary = {}
    for edu, value in file.items(): 
        edu_dictionary[edu] = {"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,
                               "ID":0, "MT":0, "LY":0,"SP":0,"OP": 0}
        for register, count in value["register"].items(): 
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
            edu_dictionary[edu][main_register] += count
    #now we have a dictionary where each educational category contains the total values of all its registers

final_dict = {}
edu_dict = {}
row_counter = 0
    #final_dict[row_counter] = [edu, main_register, percentage]
for edu, registers in edu_dictionary.items():
    total = sum(registers.values())
    edu_dict[row_counter] = [edu, total]
    for register, value in registers.items():
        final_dict[row_counter] = [edu, register, (value / total) * 100]
        row_counter +=1

df = pd.DataFrame.from_dict(final_dict, orient="index", columns=["edu","main_register","percentage"])
total_df = pd.DataFrame.from_dict(edu_dict, orient="index", columns=["edu", "percentage"])
    #two separate dataframes for two subplots 

#this defines the structure
fig = make_subplots(rows=2, cols=1, #if we swap around the numbers the charts are side by side, not one above the other
                    subplot_titles=["Percentage distribution of main registers in educational categories",
                                    "Distribution of educational categories in the dataset"],
                                    specs=[[{"type":"bar"}], [{"type":"pie"}]])
                                    #first subplot is a bar plot, the other a pie

bar_data = []
legend_check = []

for index, row in df.iterrows():
    if row["main_register"] in legend_check:                                      #legendgroups are needed so things don't repeat unnecessarily in the legend
        bar_data.append(go.Bar(name=row["main_register"], x=[row["edu"]], y=[row["percentage"]], legendgroup=str(row["main_register"]), showlegend=False))

    else:
        bar_data.append(go.Bar(name=row["main_register"], x=[row["edu"]], y=[row["percentage"]], legendgroup=str(row["main_register"])))
        legend_check.append(row["main_register"])


for item in bar_data:
    fig.add_trace(item, row=1, col=1)

fig.update_layout(barmode="stack")
fig.add_trace(go.Pie(labels=total_df["edu"], values = total_df["percentage"]), row=2, col=1)

fig.update_layout(legend_title_text='Register')

fig.show()

        