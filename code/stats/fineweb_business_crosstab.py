import json 
import numpy as np
import pandas as pd 
import scipy.stats as st

edus = []
businesses = []
sums = []
with open ("C:/Users/shkunn/Downloads/finewebs_edu.txt", "r") as f:
    file = f.read()
    j = json.loads(file)
    for edu, value in j.items():
        if edu != "4" and edu != "5":
            print(edu)
            dict = {}
            for business, num in value["business"].items():
                if business in dict.keys():
                    dict[business] += num
                else:
                    dict[business] = num
            for r, n in dict.items():
                edus.append(edu)
                businesses.append(r)
                sums.append(n)
            continue
        if edu == "4":
            dict_four_five = {}
            for business, num in value["business"].items():
                if business in dict_four_five.keys():
                    dict_four_five[business] += num
                else:
                    dict_four_five[business] = num
        if edu == "5":
            for business, num in value["business"].items():
                if business in dict_four_five.keys():
                    dict_four_five[business] += num
                else:
                    dict_four_five[business] = num

for r, n in dict_four_five.items():
    edus.append("4")
    businesses.append(r)
    sums.append(n)
        

cross_ec = pd.crosstab(columns=edus, index=businesses, values=sums, aggfunc=sum)

cross_ce = pd.crosstab(columns=businesses, index=edus, values=sums, aggfunc=sum)


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

