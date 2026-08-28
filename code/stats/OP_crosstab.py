import json
import numpy as np
import pandas as pd

#compare OP texts by edu category, figure out what explains 
edus = []
businesses = []
counts = []

with open ("C:/Users/shkunn/Downloads/pure_OP.txt") as f:
    f = f.read()
    file = json.loads(f)
    for edu, content in file.items():
        for business, count in content["business_sector"].items():
            edus.append(edu)
            businesses.append(business)
            counts.append(count)

cross = pd.crosstab(columns=edus, index=businesses, values=counts, aggfunc=sum)

# Overall profile: how items are distributed across sectors
overall_profile = cross.sum(axis=1) / cross.sum().sum()

# Each educational category's profile
column_profiles = cross.div(cross.sum(axis=0), axis=1)

# Chi-square distance of each category from the average
chi_sq_distances = {}
for col in column_profiles.columns:
    diff = column_profiles[col] - overall_profile
    distance = (diff ** 2 / overall_profile).sum()
    chi_sq_distances[col] = distance

distances = pd.Series(chi_sq_distances).sort_values(ascending=False)
print("Pure OP, business sector")
print(distances)