import json

region_counts = {}


def n_largest_values(d, N):  #d is the dictionary, N is the amount of results 
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True)[:N])

def give_proportions(dict, total):
    prop_dict = {}
    for key, value in dict.items():
        prop = value / total 
        prop_dict[key] = [value, prop]
    return prop_dict

with open ("C:/Users/shkunn/Downloads/region_output.txt") as f:
    f = f.read()
    region_dict = json.loads(f)
    for region, content in region_dict.items():
        tld = content["tld"] #dictionary with key-value pairs of tlds and numbers showing the amount of documents
        country = content["country_relevance"] 
        register = content["register"]
        total = sum(tld.values()) #gives total number of documents relating to this region 

        tld_highest = n_largest_values(tld, 5) # 5 most common tlds
        register_highest = n_largest_values(register, 5)
        country_highest = n_largest_values(country, 5)

        tld_prop = give_proportions(tld_highest, total)
        country_prop = give_proportions(country_highest, total) 
        register_prop = give_proportions(register_highest, total)
        region_counts[region] = {"total": [total, total / 51435563], "tld": tld_prop, "country_relevance": country_prop, "register": register_prop}

#sorts by frequency of registers
region_sorted = dict(sorted(region_counts.items(), key = lambda item: item[1]["total"], reverse = True))

with open ("C:/Users/shkunn/Documents/region_sorted.txt", "w") as f:
    json.dump(region_sorted, f)



    