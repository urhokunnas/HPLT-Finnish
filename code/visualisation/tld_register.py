import json
import numpy as np
import pandas as pd
import plotly.express as px
top_tlds = ["fi", "com", "net","org","eu","info","se","shop","ru","nl"] 

sort_order = {k: i for i, k in enumerate(top_tlds)}
print(sort_order)
with open ("C:/Users/shkunn/Documents/HPLT4_Finnish/counts/tld_output.txt") as f:
    f = f.read()
    file = json.loads(f)
    dictionary = {}
    row_counter = 0 
    
    
    for tld in top_tlds:
        register_dict = {}
        #key = country name
        #value["register"] = dict of register-value pairs (value is the sum of texts)
        for register, count in file[tld]["register"].items(): 
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
            dictionary[row_counter] = [tld, register, count ]
            row_counter += 1 

sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1][2])) 

final_sorted = dict(sorted(sorted_dict.items(), key=lambda item: sort_order.get(item[1][0], float('inf'))))

df = pd.DataFrame.from_dict(final_sorted, orient="index", columns=["tld","main_register","count"])

bar_fig = px.bar(df, x="tld",y="count", color="main_register", barmode="stack")

bar_fig.update_layout(legend_title_text='Register', title_text="Registers by top level domain (TLD)",
                      xaxis_title_text="Count", yaxis_title_text="TLD")
bar_fig.show()