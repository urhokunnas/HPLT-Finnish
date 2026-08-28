import json
import numpy as np
import pandas as pd
import plotly.express as px

year_dict = {"2014":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0},
             "2015":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0},
             "2016":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0},
             "2017":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0},
             "2018":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0},
             "2019":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0},
             "2020":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0},
             "2021":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0},
             "2022":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0},
             "2023":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0},
             "2024":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0},
             "2025":{"NA":0, "HI":0,"IN":0,"IP":0, "Hybrid":0,"ID":0, "MT":0, "LY":0,"SP":0,"OP": 0}}

with open ("C:/Users/shkunn/Downloads/crawl_year.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    for crawl, content in file.items():
        if "CC" not in crawl: #filters out wide and archivebot crawls 
            continue 
        year = crawl.split("-")[2]
        for edu, item in content.items():
            for register, value in item["register"].items():
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
                year_dict[year][main_register]+= value 

dict_for_df = {}
row_counter = 0

for year, content in year_dict.items():
    total = sum(content.values())
    for register, value in content.items():
        dict_for_df[row_counter] = [year, register, value/total]
        row_counter += 1

df = pd.DataFrame.from_dict(dict_for_df, orient="index", columns=["year","register","sum"])

bar = px.bar(df, x="year",y="sum",color="register",barmode="stack")

bar.update_layout(legend_title_text='Register', 
        title_text=f"Register distribution of texts by year",
                      xaxis_title_text="Year of CC crawl", yaxis_title_text="Portion of yearly total")

bar.show()