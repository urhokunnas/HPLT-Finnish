import json
import numpy as np
import pandas as pd
import plotly.express as px

edu_totals = {"none":19642994, "minimal":17556194, "basic": 9022275, "moderate": 4768090, "high": 446010 }
#total size of each educational category

with open ("C:/Users/shkunn/Downloads/edu_output.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    edu_dictionary = {}
    for edu, value in file.items(): 
        edu_dictionary[edu] = {}
        for register, sum in value["register"].items():
            if "re" in register:
                edu_dictionary[edu][register] = sum


edu_props = {}
for edu, value in edu_dictionary.items():
    edu_props[edu] = {}
    for register, sum in value.items():
        edu_props[edu][register] = sum / edu_totals[edu]
#get charts like this for all registers then do the same but with equalised bars so it's easier to compare changes in proportion 
#between educational categories 
row_counter = 0
dict_for_df = {}
for edu, value in edu_props.items():
    for register, percent in value.items():
        dict_for_df[row_counter] = [edu, register, percent]
        row_counter += 1

df = pd.DataFrame.from_dict(dict_for_df, orient="index", columns=["edu","register","proportion"])

bar_fig = px.bar(df, x="edu",y="proportion", color="register", barmode="stack")

bar_fig.update_layout(legend_title_text='Register', 
        title_text="Distribution of recipe texts in educational categories (The total size of the bar is the proportion of re in that edu category)",
                      xaxis_title_text="Count", yaxis_title_text="Educational category")

bar_fig.show()