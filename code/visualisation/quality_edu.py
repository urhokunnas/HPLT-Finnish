import json
import numpy as np
import pandas as pd
import plotly.express as px



with open ("C:/Users/shkunn/Downloads/quality_sorted.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    dictionary = {}
    for quality, value in file.items(): 
        dictionary[quality] = {"none": 0, "minimal":0, "basic":0, "moderate":0, "high":0}
        for edu, count in value["edu"].items(): 
            dictionary[quality][edu] += count
    #now we have a dictionary where each educational category contains the total values of all its registers

final_dict = {}
qua_dict = {}
row_counter = 0
    #final_dict[row_counter] = [edu, main_register, percentage]

register_names = {"MT": "Machine translated or generated", "LY":"Lyrical",
                  "SP": "Spoken", "ID": "Interactive discussion", "NA": "Narrative",
                  "HI": "How-to or instructions", "IN": "Informational description", 
                  "OP": "Opinion", "IP": "Informational persuasion", 
                  "Hybrid":"Hybrid of multiple registers"}

#edu_percentages = {"none": 0, "minimal": 0, "basic": 0, "moderate": 0, "high": 0 }
for quality, edus in dictionary.items():
    total = sum(edus.values())
    qua_dict[row_counter] = [quality, total]
    for edu, value in edus.items():
        percent = (value / total) *100
        label = f"{round(percent, 2)} %"
        final_dict[row_counter] = [quality, edu, percent, label]
        row_counter +=1 

total_sum = 0 #total size of the dataset 
for row, item in qua_dict.items():
    total_sum += item[1]

qua_percentages = {}
for row, value in qua_dict.items():
    p = (value[1] / total_sum) * 100
    qua_percentages[value[0]] = round(p, 2)


for row, value in final_dict.items():
    qual = value[0]
    bar_label = f"{qual} ({qua_percentages[qual]})%"
    final_dict[row].append(bar_label)
df = pd.DataFrame.from_dict(final_dict, orient="index", columns=["quality","edu","percentage", "text", "bar_label"])


fig = px.bar(df, x="bar_label", y="percentage", color="edu", barmode="stack", text="text")

fig.update_layout(font_size = 18,
                    legend_title_text='Propella-4b educational value', 
                      yaxis_title_text="Percent", xaxis_title_text="Propella-4b quality (percent of total dataset)",
                      legend=dict(orientation="h", yanchor="bottom", y=1),legend_title_side = "top center",
                      yaxis = dict(tickmode = "linear", tick0 = 0, dtick = 5, ticklabelstep=2))

fig.show()