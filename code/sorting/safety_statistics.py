import json

safety_counts = {}

def n_largest_values(d, N):
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True)[:N]) #d is the dictionary, N is the amount of results 

def give_proportions(dict, total):
    prop_dict = {}
    for key, value in dict.items():
        prop = int(value) / int(total) 
        prop_dict[key] = [value, prop]
    return prop_dict

with open ("C:/Users/shkunn/Downloads/safety_output.txt", "r") as f:
    file = f.read()
    safety_dict = json.loads(file)
    for safety, content in safety_dict.items():
        safety_counts[safety] = {}
        register = content["register"] #dictionary with key-value pairs of registers and numbers showing the amount of documents
        region = content["regional_relevance"] 
        country = content["country_relevance"]
        tld = content["tld"]
        edu = content["educational_value"]
        total = sum(tld.values()) #total size of that edu category

        register_highest = n_largest_values(register, 10) # 10 most common registers
        country_highest = n_largest_values(country, 10)
        region_highest = n_largest_values(region,10)
        tld_highest = n_largest_values(tld, 10)
        edu_highest = n_largest_values(edu, 10)

        register_prop = give_proportions(register_highest, total)
        region_prop = give_proportions(region_highest, total) 
        country_prop = give_proportions(country_highest, total)
        tld_prop = give_proportions(tld_highest, total)
        edu_prop = give_proportions(edu_highest, total)

        safety_counts[safety] = {"total": [total, total / 51435563 ], "register": register_prop,
                           "regional_relevance": region_prop, "country_relevance": country_prop,
                           "tld": tld_prop, "educational_value": edu_prop}
    
safety_sorted = dict(sorted(safety_counts.items(), key = lambda item: item[1]["total"][0], reverse = True))

with open("C:/Users/shkunn/Documents/results/sorted/safety_sorted.txt", "w") as f:
    json.dump(safety_sorted, f)

with open("C:/Users/shkunn/Documents/results/sorted/safety_sorted.txt") as f:
    file = f.read()
    full = json.loads(file)
    with open("C:/Users/shkunn/Documents/results/top_values/safety_stats.txt", "a") as output:
        for key, value in full.items():
            tlds = {k: value["tld"][k] for k in list(value["tld"])[:5]}
            regions = {k: value["regional_relevance"][k] for k in list(value["regional_relevance"])[:5]}
            registers = {k: value["register"][k] for k in list(value["register"])[:5]}
            countries = {k: value["country_relevance"][k] for k in list(value["country_relevance"])[:5]}
            educations = {k: value["educational_value"][k] for k in list(value["educational_value"])[:5]}

            output.write(f"{key}: Amount of documents: {value["total"]}. Top registers: {registers}\n Top tlds: {tlds} \n Top countries: {countries} \n Top regions: {regions} \n Top educational labels {educations} \n \n ")
