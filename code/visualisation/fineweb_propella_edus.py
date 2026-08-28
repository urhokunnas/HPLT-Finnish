import json
import numpy as np
import pandas as pd
import plotly.express as px



with open ("C:/Users/shkunn/Downloads/finewebs_edu.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    edu_dictionary = {}
    for edu, value in file.items(): 
        if edu == "5":
            edu  = "4"
        edu_dictionary[edu] = {"none": 0, "minimal":0, "basic":0, "moderate":0,
                               "high":0}
        for prop_edu, count in value["prop_edu"].items(): 
            edu_dictionary[edu][prop_edu] += count
    #now we have a dictionary where each educational category contains the total values of all its registers

final_dict = {}
edu_dict = {}
row_counter = 0
    #final_dict[row_counter] = [edu, main_register, percentage] 
 
fineweb_labels = {"-0": "-1–0", "0": "0–1", "1": "1–2", "2":"2–3", "3": "3–4", "4": "4–5"}
#edu_percentages = {"none": 0, "minimal": 0, "basic": 0, "moderate": 0, "high": 0 }
for edu, registers in edu_dictionary.items():
    total = sum(registers.values())
    edu_dict[row_counter] = [edu, total]
    for prop, value in registers.items():
        percent = (value / total) *100
        label = f"{round(percent, 3)} %"
        fullname = fineweb_labels[edu]
        final_dict[row_counter] = [edu, fullname, prop, percent, label]
        row_counter +=1 

total_sum = 0 #total size of the dataset 
for row, item in edu_dict.items():
    total_sum += item[1]

edu_percentages = {}
for row, value in edu_dict.items():
    p = (value[1] / total_sum) * 100
    edu_percentages[value[0]] = round(p, 2)


for row, value in final_dict.items():
    educ = value[0]
    fullname = value[1]
    if fullname == "4–5":
        bar_label = "4–5 (<0.001%)"
    else:
        bar_label = f"{fullname} ({edu_percentages[educ]} %)"
    final_dict[row].append(bar_label)
df = pd.DataFrame.from_dict(final_dict, orient="index", columns=["edu","fullname","propella","percentage", "text", "bar_label"])


fig = px.bar(df, x="bar_label", y="percentage", color="propella", barmode="stack", text="text")

fig.update_layout(font_size = 18,
                    legend_title_text='Propella-4b educational value', 
                      yaxis_title_text="Percent", xaxis_title_text="Finewebs educational value (portion of total data)",
                      legend=dict(orientation="h", yanchor="bottom", y=1),legend_title_side = "top center",
                      xaxis_categoryorder = "category ascending",
                      yaxis = dict(tickmode = "linear", tick0 = 0, dtick = 5, ticklabelstep=2))

fig.show()