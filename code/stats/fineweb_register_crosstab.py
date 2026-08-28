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

edus = []
registers = []
sums = []
with open ("C:/Users/shkunn/Downloads/finewebs_edu.txt", "r") as f:
    file = f.read()
    j = json.loads(file)
    for edu, value in j.items():
        if edu != "4" and edu != "5":
            print(edu)
            dict = {}
            for register, num in value["register"].items():
                reg = return_main(register)
                if reg in dict.keys():
                    dict[reg] += num
                else:
                    dict[reg] = num
            for r, n in dict.items():
                edus.append(edu)
                registers.append(r)
                sums.append(n)
            continue
        if edu == "4":
            dict_four_five = {}
            for register, num in value["register"].items():
                reg = return_main(register)
                if reg in dict_four_five.keys():
                    dict_four_five[reg] += num
                else:
                    dict_four_five[reg] = num
        if edu == "5":
            for register, num in value["register"].items():
                reg = return_main(register)
                if reg in dict_four_five.keys():
                    dict_four_five[reg] += num
                else:
                    dict_four_five[reg] = num

for r, n in dict_four_five.items():
    edus.append("4")
    registers.append(r)
    sums.append(n)
        

cross_ec = pd.crosstab(columns=edus, index=registers, values=sums, aggfunc=sum)

cross_ce = pd.crosstab(columns=registers, index=edus, values=sums, aggfunc=sum)


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

