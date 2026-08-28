import json 
import numpy as np
import pandas as pd 
import plotly.express as px 

edu_dict = {}
row_counter = 0
with open ("C:/Users/shkunn/Downloads/content_condensed.txt", "r") as f:
    file = f.read()
    doc = json.loads(file)
    for type, value in doc.items():
        for i in ["none", "minimal", "basic", "moderate", "high"]:
            sum = value["edu"][i]
            edu_dict[row_counter] = [type, i, sum]
            row_counter += 1

df = pd.DataFrame.from_dict(edu_dict, orient="index", columns=["content_type","educational_value","sum"])

fig = px.bar(df, x="content_type",y="sum", color="educational_value", barmode="stack")

fig.update_layout(legend_title_text='Educational value',
                      xaxis_title_text="Content type", 
                      yaxis_title_text="Sum",
                      font_size=14,
                      xaxis_categoryorder="total descending")

fig.show()
