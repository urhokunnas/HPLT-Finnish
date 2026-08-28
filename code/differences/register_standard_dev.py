import json
import statistics

# pull standard deviations of values to show how much different things vary 

countries = {}   #keys are names of countries
tlds = {}
regions = {}

#the file contains a dictionary with registers as keys, values are dictionaries of the form:
#{"tld":{"com":32566, "fi":46062}, "regional_relevance":{"europeam":5543, "global":456022}, "country_relevance":{"finland":13555, "norway":124}}
with open ("C:/Users/shkunn/Downloads/register_output.txt") as file:
    f = file.read()
    f_json = json.loads(f)
    for register, content in f_json.items():
        country = content["country_relevance"]        #dictionary of country: 12345 key-value pairs
        tld = content["tld"]
        region = content["regional_relevance"]
        total = sum(tld.values())
        
        for item, value in country.items(): 
            if item in countries.keys():
                countries[item]["totals"].append(value)
                countries[item]["proportions"].append(value / total)
            else:
                countries[item] = {"totals": [value], "proportions": [value / total]}
        for item, value in tld.items():
            if item in tlds.keys():
                tlds[item]["totals"].append(value)
                tlds[item]["proportions"].append(value / total)
            else:
                tlds[item] = {"totals": [value], "proportions": [value / total]}
        for item, value in region.items():
            if item in regions.keys():
                regions[item]["totals"].append(value)
                regions[item]["proportions"].append(value / total)
            else:
                regions[item] = {"totals": [value], "proportions": [value / total]}

country_stats = [] #keys: countries. values: {standard deviation: 0.00, mean: 0.00, total: 000  }
tld_stats = []
region_stats = []
for item, value in countries.items(): #value = {"totals:" [12234, 1234, etc.], "proportions": [0.2, 0.45, 0.002 etc.]}
    try:
        country_stats.append({"country": item,
                        "stdev":statistics.stdev(value["proportions"]), 
                       "mean": statistics.mean(value["proportions"]), "total": sum(value["totals"])} )
    except:
        print(f"Issue with country {item}")
for item, value in tlds.items(): #value = {"totals:" [12234, 1234, etc.], "proportions": [0.2, 0.45, 0.002 etc.]}
    try:
        tld_stats.append({"tld": item,
                        "stdev":statistics.stdev(value["proportions"]), 
                       "mean": statistics.mean(value["proportions"]), "total": sum(value["totals"])} )
    except:
        print(f"Issue with tld {item}")
for item, value in regions.items(): #value = {"totals:" [12234, 1234, etc.], "proportions": [0.2, 0.45, 0.002 etc.]}
    try:
        region_stats.append({"region": item,
                        "stdev":statistics.stdev(value["proportions"]), 
                       "mean": statistics.mean(value["proportions"]), "total": sum(value["totals"])} )
    except:
        print(f"Issue with region {item}")

country_stats.sort(key=lambda x: x["stdev"], reverse=True)
tld_stats.sort(key=lambda x: x["stdev"], reverse=True)
region_stats.sort(key=lambda x: x["stdev"], reverse=True)

with open ("C:/Users/shkunn/Documents/results/differences/register_country_stdev.txt", "a") as f:
    f.write("Top 50 countries by standard deviation within registers:\n")
    for d in country_stats[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/differences/register_tld_stdev.txt", "a") as f:
    f.write("Top 50 tlds by standard deviation within registers:\n")
    for d in tld_stats[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/differences/register_region_stdev.txt", "a") as f:
    f.write("Top 50 regions by standard deviation within registers:\n")
    for d in region_stats[:50]:
       json.dump(d,f)
       f.write("\n\n")
 