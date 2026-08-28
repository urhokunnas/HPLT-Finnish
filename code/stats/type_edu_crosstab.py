import json 
import numpy as np
import pandas as pd 
import scipy.stats as st

types = []
edus = []
sums = []
with open ("C:/Users/shkunn/Downloads/content_condensed.txt", "r") as f:
    file = f.read()
    j = json.loads(file)
    for type, value in j.items():
        for edu, num in value["edu"].items():
            types.append(type)
            edus.append(edu)
            sums.append(num)

cross_ec = pd.crosstab(columns=edus, index=types, values=sums, aggfunc=sum)

cross_ce = pd.crosstab(columns=types, index=edus, values=sums, aggfunc=sum)


for cross in [cross_ec, cross_ce]:
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
    print(distances)

