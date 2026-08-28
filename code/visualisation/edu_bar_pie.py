import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots 

with open ("C:/Users/shkunn/Downloads/edu_output.txt") as f:
    f = f.read()
    file = json.loads(f)
    for key, value in file.items():
        #key: edu value. make separate dictionaries for each one 
        #value: dict of data, the only relevant one is value["register"], which in turn is a dict
        dictionary = {}   
        register_sums = {"MT":0, "LY":0, "SP":0, "ID": 0, "NA": 0, "HI": 0, "IN":0, "OP":0, "IP":0, "Hybrid":0}
        row_counter = 0
        hybrid_sum = 0
        for register, count in value["register"].items():
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
            dictionary[row_counter] = [main_register, #either "Hybrid" or one of the following: "MT", "LY", "SP","ID", "NA","HI" "IN", "OP", "IP"
                                 register, #either just a main register or something like "NA-ne" or "MT-OP-rv"
                                 count] #integer value, number of documents with that register
            register_sums[main_register] += count
            row_counter += 1
        
        sort_order = {k: i for i, k in enumerate(sorted(register_sums.items(), key=lambda x: x[1]))}

        sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1][2], reverse=True)) 
        #this sorts by subregister value, so that the subregisters of one main register
            #are in the correct relative order even if they are mixed with items from other registers
        
        final_sorted = dict(sorted(sorted_dict.items(), key=lambda item: sort_order.get(item[1][0]), reverse=True))
        #results in a dictionary where the largest main register comes first
            #and all its subregisters are sorted starting from the largest down 
            #and the same for all subregisters 
        df = pd.DataFrame.from_dict(final_sorted, orient="index", columns=["main_register","register","count"])

        Hybrid_df = df.loc[df["main_register"] == "Hybrid"]

        one_percent =register_sums["Hybrid"] / 100 #fiddle with this to make the pie charts useful
        Hybrid_df.loc[Hybrid_df["count"] < one_percent, "register" ] = "Other"

        fig = make_subplots(rows=2, cols=1,
                                     subplot_titles=[f"Distribution of registers in educational category {key}", "Hybrids of main categories"],
                                      specs=[[{"type": "bar"}], [{"type": "pie"}]])
        
        bar_data = []
        for index, row in df.iterrows():
            bar_data.append(go.Bar(name=row["register"], x=[row["main_register"]], y=[row["count"]]))

        for item in bar_data:
            fig.add_trace(item, row=1, col=1)

        fig.update_layout(barmode="stack")
        fig.add_trace(go.Pie(labels=Hybrid_df["register"], values = Hybrid_df["count"]), row=2, col=1)

        fig.update_layout(legend_title_text='Register')


        fig.show()