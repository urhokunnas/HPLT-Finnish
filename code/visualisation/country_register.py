import json
import numpy as np
import pandas as pd
import plotly.express as px
top_countries = {"none": 11,"united_states":10, "united_kingdom":9, "russia":8,
                     "germany":7, "sweden":6,"france":5, "supranational":4, "italy":3, "spain":2}

sort_order = {k: i for i, (k, _) in enumerate(sorted(top_countries.items(), key=lambda x: x[1]))}
print(sort_order)
#SORTING DOESN'T WORK IT'S WHINING ABOUT BOOLEANS AND I AM LOSING IT 
with open ("C:/Users/shkunn/Downloads/country_output.txt") as f:
    f = f.read()
    file = json.loads(f)
    dictionary = {}
    row_counter = 0 
    
    #in the interest of speeding up things this is a manually created list of the most frequent countries
    #it makes the code versatile, since it's easy to customise the countries depending on what we're interested in
    for country in top_countries:
        register_dict = {}
        #key = country name
        #value["register"] = dict of register-value pairs (value is the sum of texts)
        for register, count in file[country]["register"].items(): 
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
            if main_register in register_dict.keys():
                register_dict[main_register] += count
            else:
                register_dict[main_register] = count
        for register, count in register_dict.items():
            dictionary[row_counter] = [country, register, count ]
            row_counter += 1 

sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1][2]))
final_sorted = dict(
    sorted(sorted_dict.items(), key=lambda item: sort_order.get(item[1][0], float('inf')), reverse=True)
)
df = pd.DataFrame.from_dict(final_sorted, orient="index", columns=["country","main_register","count"])

bar_fig = px.bar(df, x="country",y="count", color="main_register", barmode="stack")

#change order of educational categories to go none, minimal, basic, moderate, high
#maybe remove the sums? but try to add percentages of total maybe
bar_fig.update_layout(legend_title_text='Register', title_text="Registers by country text relates to (top 2-11 countries, excluding Finland)",
                      xaxis_title_text="Count", yaxis_title_text="Country")
bar_fig.show()