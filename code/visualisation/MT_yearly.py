import json
import numpy as np
import pandas as pd
import plotly.express as px

targeted_register = "MT"
year_dict = {"2014":{},"2015":{},"2016":{},"2017":{},"2018":{},"2019":{},"2020":{},
             "2021":{},"2022":{},"2023":{},"2024":{},"2025":{}}

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
                    year_dict[year][register] = value

dict_even = {}
row_counter = 0

for year, content in year_dict.items():
    total = sum(content.values())
    other = 0
    for register, value in content.items():
        if value/total < 0.01:
              other += value
        else: 
            dict_even[row_counter] = [year, register, value/total]
            row_counter += 1
    dict_even[row_counter] = [year, "Other register", other/total]
    row_counter += 1

df = pd.DataFrame.from_dict(dict_even, orient="index",columns=["year","register","proportion"])

bar = px.bar(df,x="year",y="proportion",color="register",barmode="stack")

bar.update_layout(legend_title_text='Register', 
        title_text=f"Distribution of {targeted_register} texts by year",
                      xaxis_title_text="Count", yaxis_title_text="Year of CC crawl")

bar.show()