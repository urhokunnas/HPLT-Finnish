import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots 

with open ("C:/Users/shkunn/Downloads/edu_output.txt") as f:
    f = f.read()
    file = json.loads(f)
    for key, value in file.items():
        #key: edu value. make separate dictionaries for each one 
        #value: dict of data, the only relevant one is value["register"], which in turn is a dict
        dictionary = {}   # would like to name this after the edu value but maybe i can sidestep that 
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
                    hybrid_sum += count
            dictionary[row_counter] = [main_register, #either "Hybrid" or one of the following: "MT", "LY", "SP","ID", "NA","HI" "IN", "OP", "IP"
                                 register, #either just a main register or something like "NA-ne" or "MT-OP-rv"
                                 count] #integer value, number of documents with that register
            row_counter += 1
        sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1][2], reverse=True))
        df = pd.DataFrame.from_dict(sorted_dict, orient="index", columns=["main_register","register","count"])
        pie_df = pd.DataFrame.from_dict(sorted_dict, orient="index", columns=["main_register","register","count"])

        one_percent = hybrid_sum / 100 #fiddle with this to make the pie charts useful
        pie_df.loc[pie_df["count"] < one_percent, "register" ] = "Other"

        bar_fig = px.bar(df, x="main_register",y="count", color="register", title=key)
        bar_fig.update_layout(xaxis={'categoryorder':'total descending'}, template="plotly_white")


        pie_fig = px.pie(pie_df.loc[df["main_register"] == "Hybrid"], values = "count", names = "register", title=key)

        combined_fig = make_subplots(rows=2, cols=1, vertical_spacing=0.5,
                                     subplot_titles=[key, "Hybrid"],
                                      specs=[[{"type": "bar"}], [{"type": "pie"}]])

        
        bar_traces = []
        pie_traces = []
        for trace in range(len(bar_fig["data"])):
            bar_traces.append(bar_fig["data"][trace])
        for trace in range(len(pie_fig["data"])):
            pie_traces.append(pie_fig["data"][trace])


        for traces in bar_traces:
            combined_fig.append_trace(traces, row = 1, col = 1)
            #why are you not stacked 
            #would also like to combine the 'other' category to make the bar chart easier to read
            #also the bar chart is tiny and difficult to see -> fix 
                #if i can't make this work i might just keep the bar and pie charts separate
                #but this is pretty neat 
        for traces in pie_traces:
            combined_fig.append_trace(traces, row = 2, col = 1)

        combined_fig.show()
        #add labels to show the edu category and to identify that the pie chart is of hybrids
        


     


#stacked bar graph for each edu label
    # total size shows size of that edu category, but we also see the split of different registers
        #it would be nice to have something with the split of registers in the total dataset 
        #maybe as its own bar chart?
        #since next to the edu ones it would be really big 

