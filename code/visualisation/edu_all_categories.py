import json
import numpy as np
import pandas as pd
import plotly.express as px

with open ("C:/Users/shkunn/Downloads/edu_output.txt") as f:
    f = f.read()
    file = json.loads(f)
    dictionary = {}
    row_counter = 0 
    for edu, value in file.items():
        #key = edu value
        #value["register"] = dict of register-value pairs (value is the sum of texts)
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
            dictionary[row_counter] = [edu, main_register, count ]
            row_counter += 1 

print(dictionary)
df = pd.DataFrame.from_dict(dictionary, orient="index", columns=["edu","main_register","count"])

print(df)
bar_fig = px.histogram(df, x="edu",y="count", color="main_register", barmode="stack",text_auto=True)

#change order of educational categories to go none, minimal, basic, moderate, high
#maybe remove the sums? but try to add percentages of total maybe
bar_fig.update_layout(legend_title_text='Register', title_text="Registers by educational value of text",
                      xaxis_title_text="Count", yaxis_title_text="Educational value")
bar_fig.show()
print("plotly express hover template:", bar_fig.data[0].hovertemplate)
