import json
import numpy as np
import pandas as pd
import plotly.express as px

# stacked bar chart where all the bars are equally sized 
#contain all registers with MT in them + a big portion is "Everything else", so you can see both the proportion of MT texts
#(including MT hybrids) and what the composition of that group is like 

targeted_register = "MT"
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
    other = 0
    for register, value in content.items():
        dict_even[row_counter] = [year, register, value]
        row_counter += 1
    row_counter += 1

for year, value in non_dict.items():
    dict_even[row_counter] = [year, "Not IP", value]
    row_counter += 1
    yearly_totals[year] += value


dict_percent = {}

for row, item in dict_even.items():
    portion = item[2] / yearly_totals[item[0]]
    percent = portion * 100
    dict_percent[row] = [item[0], item[1], percent]


df = pd.DataFrame.from_dict(dict_percent, orient="index",columns=["year","register","proportion"])

bar = px.bar(df,x="year",y="proportion",color="register",barmode="stack")

bar.update_layout(legend_title_text='Register', 
        title_text=f"Distribution of {targeted_register} texts by year",
                      xaxis_title_text="Year of CC crawl", yaxis_title_text="%")

bar.show()