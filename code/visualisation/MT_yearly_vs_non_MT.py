import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
# stacked bar chart where all the bars are equally sized 
#contain all registers with MT in them + a big portion is "Everything else", so you can see both the proportion of MT texts
#(including MT hybrids) and what the composition of that group is like 

cutoff = 0.5 #how small registers must be to be considered "other"
targeted_register = "IN"
year_dict = {"2014":{},"2015":{},"2016":{},"2017":{},"2018":{},
             "2019":{},"2020":{},
             "2021":{},"2022":{},"2023":{},"2024":{},"2025":{}}

non_dict = {}
yearly_totals = {}

with open ("C:/Users/shkunn/Downloads/crawl_year.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    for crawl, content in file.items():
        if "CC" not in crawl: #filters out wide and archivebot crawls 
            continue 
        year = crawl.split("-")[2]
        for edu, item in content.items():
            for register, value in item["register"].items():
                if targeted_register in register:
                    if register in year_dict[year].keys():
                        year_dict[year][register] += value
                    else:
                        year_dict[year][register] = value
                else:
                    if year in non_dict.keys():
                        non_dict[year] += value
                    else:
                        non_dict[year] = value

dict_even = {}
row_counter = 0

for year, content in year_dict.items():
    total = sum(content.values())
    yearly_totals[year] = total
    for register, value in content.items():
        dict_even[row_counter] = [year, register, value]
        row_counter += 1
    row_counter += 1


for year, value in non_dict.items():
    yearly_totals[year] += value

dict_percent = {}
dict_other = {}
other_registers = []
good_registers = []
dict_other_registers = {}
for row, item in dict_even.items():
    portion = item[2] / yearly_totals[item[0]]
    percent = portion * 100
    for reg in good_registers:
        if item[1] == reg:
            dict_percent[row] = [item[0], item[1], percent, "big"]
            continue
    for reg in other_registers:
        if item[1] == reg:
            if item[0] in dict_other.keys(): 
                dict_other[item[0]] += percent 
                dict_other_registers[row] = [item[0], item[1], percent]
            else:                               
                dict_other[item[0]] = percent
                dict_other_registers[row] = [item[0], item[1], percent]
            continue
    if percent < cutoff: #can't use the same limit for all registers. also needs to make so that if the register is over the limit
        if item[0] in dict_other.keys(): #in at least one year it is shown every year
            dict_other[item[0]] += percent
            dict_other_registers[row] = [item[0], item[1], percent]          
             #if we keep info about the year and register name could make a second bar chart
        else:                               #that "zooms" into the Other category 
            dict_other[item[0]] = percent
            other_registers.append(item[1])
            dict_other_registers[row] = [item[0], item[1], percent]
    else:
        dict_percent[row] = [item[0], item[1], percent, "big"]
        good_registers.append(item[1])



for row, item in dict_other_registers.items():
    dict_percent[row] = [item[0], item[1], item[2], "other"]

for year, item in dict_other.items():
    dict_percent[row_counter] = [year, f"Other {targeted_register} (less than 0.3%)", item, "big"]
    row_counter += 1
for year, value in non_dict.items():
    portion = value / yearly_totals[year]
    percent = portion * 100
    dict_percent[row_counter] = [year, f"Not {targeted_register}", percent, "big" ]
    row_counter += 1

print(f"Good registers: {good_registers}")
print(f"Other registers:{other_registers}")
df = pd.DataFrame.from_dict(dict_percent, orient="index",columns=["year","register","%", "type"])

bar = px.bar(df,x="year",y="%",color="register",barmode="stack", facet_row="type",
              color_discrete_sequence=px.colors.qualitative.Alphabet)

bar.update_layout(legend_title_text='Register', 
        title_text=f"Distribution of {targeted_register} texts by year",
                      xaxis_title_text="Year of CC crawl", yaxis_title_text="%" )


bar.update_yaxes(matches=None)


bar.show()