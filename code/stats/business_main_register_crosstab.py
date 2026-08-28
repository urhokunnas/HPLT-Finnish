import json 
import numpy as np
import pandas as pd 
import scipy.stats as st 

def return_main(register):
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
    return main_register

with open ("C:/Users/shkunn/Documents/results/sorted/business_sorted.txt", "r") as f:
    businesses = []
    main_regs = []
    sums = []
    f = f.read()
    file = json.loads(f)
    for business, content in file.items():
        for register, value in content["educational_value"].items():
            main_register = return_main(register)
            businesses.append(business)
            main_regs.append(main_register)
            sums.append(value[0])


cross_br = pd.crosstab(columns=businesses, index=main_regs, values=sums, aggfunc=sum)
cross_rb = pd.crosstab(columns=main_regs, index=businesses, values=sums, aggfunc=sum)

for cross in [cross_br, cross_rb]:
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