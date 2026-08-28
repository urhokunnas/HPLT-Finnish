import json
import numpy as np
import pandas as pd
import plotly.express as px

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

MT_dict = {}
MT_avg = {}
hybrid_avg = {}
row_counter = 0
with open ("C:/Users/shkunn/Documents/HPLT4_Finnish/counts/MT_probability.txt") as f:
    f = f.read()
    file = json.loads(f)
    for year, content in file.items(): #content = [register, MT probability]
        MT_avg[year] = []
        hybrid_avg[year] = []
        for doc in content:
            register = doc[0]
            prob = doc[1]
            main_register = return_main(register)
            if main_register == "Hybrid" and "MT" in register:
                MT_dict[row_counter] = [year, prob, "Hybrid"] 
                row_counter += 1
                hybrid_avg[year].append(prob)
            elif main_register == "MT":
                MT_dict[row_counter] = [year, prob, "MT"]
                row_counter += 1
                MT_avg[year].append(prob)


for year, probs in MT_avg.items():
    avg = np.average(probs)
    print(f"Average pure MT probability in {year}: {avg}")

for year, probs in hybrid_avg.items():
    avg = np.average(probs)
    print(f"Average MT hybrid probability in {year}: {avg}")

MT_df = pd.DataFrame.from_dict(MT_dict, orient="index", columns=["year", "MT_probability", "main_register"])

MT_df.sort_values(by=["year"],inplace=True)

box= px.box(MT_df, x="year", y="MT_probability", facet_row="main_register", points=False)

box.update_layout(legend_title_text="Yearly distribution of MT probability in texts labelled as MT")
box.show()
MT_hist = px.histogram(MT_df, x="MT_probability",nbins=60, color="main_register", facet_col="year", facet_col_wrap=4)

MT_hist.update_layout(legend_title_text='Main register', 
        title_text="Yearly distribution of MT probability in texts labeled as MT",
                      yaxis_title_text="Count", xaxis_title_text="MT probability")
MT_hist.show()
