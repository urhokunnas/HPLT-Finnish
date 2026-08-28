import json 
import numpy as np
import pandas as pd 
import scipy.stats as st 

with open ("C:/Users/shkunn/Documents/results/sorted/business_sorted.txt", "r") as f:
    businesses = []
    edus = []
    sums = []
    f = f.read()
    file = json.loads(f)
    for business, content in file.items():
        for edu, value in content["educational_value"].items():
            businesses.append(business)
            edus.append(edu)
            sums.append(value[0])


cross_margins = pd.crosstab(columns=businesses, index=edus, values=sums, aggfunc=sum, margins=True)
cross_plain = pd.crosstab(columns=businesses, index=edus, values=sums, aggfunc=sum)

cross = pd.crosstab(columns=edus, index=businesses, values=sums, aggfunc=sum)

edu_order = ["none", "minimal","basic","moderate","high"]
sorted_cross = cross_plain.reindex(edu_order)

ch = st.chisquare(cross_plain)

con = st.chi2_contingency(cross_plain)

# Overall profile: how items are distributed across sectors
overall_profile = cross_plain.sum(axis=1) / cross_plain.sum().sum()

# Each educational category's profile
column_profiles = cross_plain.div(cross_plain.sum(axis=0), axis=1)

# Chi-square distance of each category from the average
chi_sq_distances = {}
for col in column_profiles.columns:
    diff = column_profiles[col] - overall_profile
    distance = (diff ** 2 / overall_profile).sum()
    chi_sq_distances[col] = distance

distances = pd.Series(chi_sq_distances).sort_values(ascending=False)
print(distances)
