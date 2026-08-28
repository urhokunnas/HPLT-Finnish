import json
import numpy as np
import pandas as pd
import plotly.express as px
import joblib

#dict[row_counter] = business, count, type

# type: one of all, high, FW3+ 

# all: every single text tagged as that business
#high: every text tagged as that business and propella high edu
#FW3+ every text tagged as that business and FW 3, 4 or 5 
diction = {}
row_counter = 0
businesses = []
full_total = 51435563
prop_total = 446010
fw_total = 5143556
proportions = {}

with open ("C:/Users/shkunn/Downloads/business_sector.txt") as f:
    file = f.read()
    business_dict = json.loads(file)
    for business, value in business_dict.items():
        if business not in businesses:
            businesses.append(business) #list of business sector names
        total = sum(value["educational_value"].values())
        diction[row_counter] = [business, total, "all","Full distribution"]
        proportions[business] = total / full_total
        row_counter += 1
        if "high" in value["educational_value"].keys():
            htotal = value["educational_value"]["high"]
            if htotal/prop_total > proportions[business]:
                colour = "Higher than full distribution"
            elif htotal/prop_total < proportions[business]:
                colour = "Lower than full distribution"
            else:
                colour = "Full distribution"
            diction[row_counter] = [business, htotal, "high", colour]
            row_counter += 1
"""
with open ("C:/Users/shkunn/Downloads/finepdfs_topten.txt") as f:
    file = json.load(f)
    for b in businesses:
        ftotal = 0
        for i in file:
            if b in i[2]:
                ftotal += 1
        if ftotal/fw_total > proportions[b]:
            colour = "Higher than full distribution"
            #print(f"{b}: {ftotal/fw_total} higher than {proportions[b]}")
        elif ftotal/fw_total < proportions[b]:
            colour = "Lower than full distribution"
            #print(f"{b}: {ftotal/fw_total} lower than {proportions[b]}")
        else:
            colour = "Full distribution"
        diction[row_counter] = [b, ftotal, "fw", colour]
        row_counter += 1
"""
file = joblib.load("C:/Users/shkunn/Downloads/bs_single.joblib")
for b in businesses:
    ftotal = file[4][b]
    if ftotal/prop_total > proportions[b]:
        colour = "Higher than full distribution"
        #print(f"{b}: {ftotal/fw_total} higher than {proportions[b]}")
    elif ftotal/prop_total < proportions[b]:
        colour = "Lower than full distribution"
        #print(f"{b}: {ftotal/fw_total} lower than {proportions[b]}")
    else:
        colour = "Full distribution"
    diction[row_counter] = [b, ftotal, "fw", colour]
    row_counter += 1



order = ["general_interest", 
"media_entertainment",
"government_public",
"retail_commerce",
"consumer_goods",
"healthcare_medical",
"hospitality_tourism",
"education_sector",
"real_estate_construction",
"nonprofit_ngo",
"technology_software",
"food_beverage_hospitality",
"manufacturing_industrial",
"consulting_professional",
"financial_services",
"academic_research",
"automotive_industry",
"advertising_marketing",
"agriculture_food",
"hardware_electronics",
"environmental_services",
"human_resources",
"legal_services",
"transportation_logistics",
"gambling_betting",
"gaming_industry",
"energy_utilities",
"travel_aviation",
"telecommunications",
"pharmaceutical_biotech",
"security_cyber",
"chemicals_materials",
"aerospace_defense",
"wholesale_distribution",
"insurance_industry",
"mining_resources",
"other"
]


df = pd.DataFrame.from_dict(diction, orient="index", columns=["business","total","type", "colour"])

fig = px.bar(df, x="business",y="total",facet_row="type", color="colour", height=900,log_y=True,  facet_row_spacing=0.1,
             color_discrete_sequence=['#636EFA','#EF553B', '#FECB52'])


fig.update_layout(font_size = 17,
                      xaxis_title_text="Business sector (Propella)",
                      xaxis_categoryorder = "array", xaxis_categoryarray = order,
                     legend=dict(orientation="h", yanchor="bottom", y=1),legend_title_side = "top left",
                     legend_title_text="")


fig.for_each_annotation(lambda a: a.update(text=""))

fig.update_layout({'yaxis': dict(matches=None,tickmode = "linear", tick0 = 0, dtick = 1, ticklabelstep=1, title_text="")})
fig.update_layout({'yaxis2': dict(matches=None,tickmode = "linear", tick0 = 0, dtick = 1, ticklabelstep=1, title_text="")})
fig.update_layout({'yaxis3': dict(matches=None,tickmode = "linear", tick0 = 0, dtick = 1, ticklabelstep=1, title_text="")})

fig.show()
