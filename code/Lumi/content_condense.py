import json 
import numpy as np
import pandas as pd 
import plotly.express as px

dict = {}
with open("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/content_type.txt", "r") as f:
    file = f.read()
    doc = json.loads(file)
    for line, item in doc.items():
        edu = item[0]
        content_type = item[1]
        register = item[2]
        business_sector = item[3]
        for type in content_type:
            if type not in dict.keys():
                dict[type] = {"edu": {}, "register":{},"business_sector":{}}

            if edu in dict[type]["edu"].keys():
                dict[type]["edu"][edu] += 1
            else:
                dict[type]["edu"][edu] = 1

            if register in dict[type]["register"].keys():
                dict[type]["register"][register] += 1
            else:
                dict[type]["register"][register] = 1

            for business in business_sector:
                if business in dict[type]["business_sector"].keys():
                    dict[type]["business_sector"][business] += 1
                else:
                    dict[type]["business_sector"][business] = 1

with open ("/scratch/project_462001491/urho/hplt_4.0/code_and_outputs/content_condensed", "w") as f:
    json.dump(dict, f)
