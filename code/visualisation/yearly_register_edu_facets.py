import json
import numpy as np
import pandas as pd
import plotly.express as px

year_dict= {"2014":{},"2015":{},"2016":{},"2017":{},"2018":{},
            "2019":{},"2020":{},"2021":{},"2022":{},"2023":{},"2024":{},"2025":{}}

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
                if edu in year_dict[year].keys():
                    if main_register in year_dict[year][edu].keys():
                        year_dict[year][edu][main_register]+= value
                    else:
                        year_dict[year][edu][main_register]= value
                else:
                    year_dict[year][edu] = {}
                    year_dict[year][edu][main_register] = value
               
dict_for_df = {}
row_counter = 0

for year, content in year_dict.items():
    for edu, registers in content.items():
        total = sum(registers.values())
        for register, value in registers.items():
            dict_for_df[row_counter] = [year, edu, register, (value/total) *100]
            row_counter += 1 

df = pd.DataFrame.from_dict(dict_for_df, orient="index", columns=["year","edu","register","percent"])

bar = px.bar(df, x="year",y="percent",color="register",barmode="stack",facet_row="edu")

bar.update_layout(legend_title_text="Register",
                  title_text="Yearly distribution of registers by educational category",
                  xaxis_title_text="Year of CC crawl")

bar.show()