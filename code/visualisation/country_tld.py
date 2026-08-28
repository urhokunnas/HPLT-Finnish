import json
import numpy as np
import pandas as pd
import plotly.express as px
top_countries = {"none": 11,"united_states":10, "united_kingdom":9, "russia":8,
                     "germany":7, "sweden":6,"france":5, "supranational":4, "italy":3, "spain":2}

sort_order = {k: i for i, (k, _) in enumerate(sorted(top_countries.items(), key=lambda x: x[1]))}
print(sort_order)
with open ("C:/Users/shkunn/Downloads/country_output.txt") as f:
    f = f.read()
    file = json.loads(f)
    dictionary = {}
    row_counter = 0 
    
    #in the interest of speeding up things this is a manually created list of the most frequent countries
    #it makes the code versatile, since it's easy to customise the countries depending on what we're interested in
    for country in top_countries:
        for tld, count in file[country]["tld"].items(): 
            dictionary[row_counter] = [country, tld, count ]
            row_counter += 1 

#sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1][2]))
final_sorted = dict(
    sorted(dictionary.items(), key=lambda item: int(sort_order.get(item[1][0])), reverse=True)
)
df = pd.DataFrame.from_dict(final_sorted, orient="index", columns=["country","tld","count"])

bar_fig = px.bar(df, x="country",y="count", color="tld", barmode="stack")

#change order of educational categories to go none, minimal, basic, moderate, high
#maybe remove the sums? but try to add percentages of total maybe
bar_fig.update_layout(legend_title_text='Top level domain (TLD)', title_text="Distribution of top level domains in texts relating to countries",
                      xaxis_title_text="Count", yaxis_title_text="Country")
bar_fig.show()