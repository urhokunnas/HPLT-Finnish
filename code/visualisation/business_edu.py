import json
import numpy as np 
import pandas as pd
import plotly.express as px

top_sectors = ["general_interest", "government_public", "consumer_goods",
               "hospitality_tourism", "real_estate_construction",
               "technology_software", "manufacturing_industrial", 
                "financial_services", "automotive_industry",
                "agriculture_food", "environmental_services",
                "legal_services", "gambling_betting"                                            
                ]

with open ("C:/Users/shkunn/Documents/results/sorted/business_sorted.txt", "r") as f:
    f = f.read()
    file = json.loads(f)
    dictionary = {}
    row_counter = 0

    for sector in top_sectors:
        total = file[sector]["total"][0]
        for education, count in file[sector]["educational_value"].items():
            if education == "high":
                type = "Row 2"
                
            else:
                type = "Row 1"
            percent = (count[0] / total) *100 
            label = f"{round(percent, 2)} %"
            dictionary[row_counter] = [sector, education, count[1], type, label]
            row_counter += 1

df = pd.DataFrame.from_dict(dictionary, orient="index", columns=["business_sector", "educational_value","count", "type", "label"])


bar_fig = px.bar(df, x="business_sector", y="count", color="educational_value", facet_row="type", text="label")

bar_fig.update_layout(font_size= 16, legend_title_text="Educational value",
                      yaxis_title_text="Count", xaxis_title_text="Business sector",
                      legend=dict(title_text="Educational value", traceorder="reversed",
                                  orientation="h", yanchor="bottom", y=1))

#legend=dict(orientation="h", yanchor="bottom", y=1),legend_title_side = "top center",
     #                 xaxis_categoryorder = "category ascending")
bar_fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

bar_fig.update_yaxes(matches=None)

bar_fig.show()