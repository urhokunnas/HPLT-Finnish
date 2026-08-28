import json
import pandas as pd
import plotly.express as px
dict_for_df = {}
row_counter = 0

order = ["none","minimal","basic","moderate","high"]
fp_names = {"0":"<0.3771","1":"0.3771–0.8929","2":"0.8929–1.1998",
            "3":"1.1998–2.6491", "4":">2.6491"}

with open ("C:/Users/shkunn/Downloads/edu_comparison.txt", "r") as f:
    f= f.read()
    file = json.loads(f)
    for key, value in file.items():
        total = sum(value.values())
        for o in order:
            num = value[o]
            dict_for_df[row_counter] = [fp_names[key], o, (num / total) *100]
            row_counter += 1

df = pd.DataFrame.from_dict(dict_for_df, orient="index",columns=["FinePDFs-Edu score","Propella score","%"])

fig = px.bar(df, x="FinePDFs-Edu score",y="%",color="Propella score")

fig.update_layout(font_size=26, height=600,
                    legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="left", x=0.2),legend_title_side = "top center",
                                        legend_title_text="Propella educational_value",
                                        yaxis = dict(tickmode = "linear", tick0 = 0, dtick = 5, ticklabelstep=2))

fig.show()