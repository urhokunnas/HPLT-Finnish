import json
import numpy as np
import pandas as pd
import plotly.express as px
top_tlds = ["net","org","eu","info","se","shop","ru","nl"] 
#in the interest of speeding up things this is a manually created list of the most frequent countries
    #it makes the code versatile, since it's easy to customise the countries depending on what we're interested in
sort_order = {k: i for i, k in enumerate(top_tlds)}
print(sort_order)
with open ("C:/Users/shkunn/Downloads/tld_output.txt") as f:
    f = f.read()
    file = json.loads(f)
    dictionary = {}
    row_counter = 0 
    
    
    for tld in top_tlds:
        #value["register"] = dict of register-value pairs (value is the sum of texts)
        for country, count in file[tld]["country_relevance"].items():             
            dictionary[row_counter] = [tld, country, count ]
            row_counter += 1 

sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1][2])) 

final_sorted = dict(sorted(sorted_dict.items(), key=lambda item: sort_order.get(item[1][0])))

df = pd.DataFrame.from_dict(final_sorted, orient="index", columns=["tld","country","count"])

bar_fig = px.bar(df, x="tld",y="count", color="country", barmode="stack")

#change order of educational categories to go none, minimal, basic, moderate, high
#maybe remove the sums? but try to add percentages of total maybe
bar_fig.update_layout(legend_title_text='Country', title_text="Distribution of countries in TLDs",
                      xaxis_title_text="Count", yaxis_title_text="TLD")
bar_fig.show()