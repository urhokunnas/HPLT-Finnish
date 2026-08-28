import json
import numpy as np
import pandas as pd
import plotly.express as px

year_dict = {"2014":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0},
             "2015":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0},
             "2016":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0},
             "2017":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0},
             "2018":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0},
             "2019":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0},
             "2020":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0},
             "2021":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0},
             "2022":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0},
             "2023":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0},
             "2024":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0},
             "2025":{"none":0, "minimal":0,"basic":0,"moderate":0,"high":0}}
            #yes keys could also be created while going through data
            #but this gives the correct order without sorting 
with open ("C:/Users/shkunn/Downloads/crawl_year.txt", "r") as f:
    f = f.read()
    file = json.loads(f)
    for crawl, content in file.items():
        if "CC" not in crawl: #filters out wide and archivebot crawls 
            continue 
        year = crawl.split("-")[2]
        for edu, value in content.items():
            year_dict[year][edu] += sum(value["tld"].values())

row_counter = 0
dict_for_df = {}

for year, content in year_dict.items():
    total = sum(content.values())
    for edu, num in content.items():
        dict_for_df[row_counter] = [year,edu,num/total]
        row_counter += 1

df = pd.DataFrame.from_dict(dict_for_df, orient="index", columns=["year","edu","sum"])

bar = px.bar(df,x="year",y="sum",color="edu",barmode="stack")

bar.update_layout(legend_title_text='Educational value', 
        title_text="Yearly distribution of educational values",
                      xaxis_title_text="Count", yaxis_title_text="Year of Common Crawl")

bar.show()

        
    
   