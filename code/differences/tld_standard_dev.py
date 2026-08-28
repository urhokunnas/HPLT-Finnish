import json
import statistics

# pull standard deviations of values to show how much different things vary
    #maybe variance of registers within countries? would be interesting to see which registers are spread out evenly
    #at least religion probably has a big standard deviation, description with intent to sell maybe lower 

countries = {}   #keys are names of countries
registers = {}
regions = {}


with open ("C:/Users/shkunn/Downloads/tld_output.txt") as file:
    f = file.read()
    f_json = json.loads(f)
    for tld, content in f_json.items():
        country = content["country_relevance"]        #dictionary of country: 12345 key-value pairs
        register = content["register"]
        region = content["regional_relevance"]
        total = sum(register.values())
        
        for item, value in country.items(): 
            if item in countries.keys():
                countries[item]["totals"].append(value)
                countries[item]["proportions"].append(value / total)
            else:
                countries[item] = {"totals": [value], "proportions": [value / total]}
        for item, value in register.items():
            if item in registers.keys():
                registers[item]["totals"].append(value)
                registers[item]["proportions"].append(value / total)
            else:
                registers[item] = {"totals": [value], "proportions": [value / total]}
        for item, value in region.items():
            if item in regions.keys():
                regions[item]["totals"].append(value)
                regions[item]["proportions"].append(value / total)
            else:
                regions[item] = {"totals": [value], "proportions": [value / total]}

country_stats = [] #keys: countries. values: {standard deviation: 0.00, mean: 0.00, total: 000  }
register_stats = []
region_stats = []
for item, value in countries.items(): #value = {"totals:" [12234, 1234, etc.], "proportions": [0.2, 0.45, 0.002 etc.]}
    try:
        country_stats.append({"country": item,
                        "stdev":statistics.stdev(value["proportions"]), 
                       "mean": statistics.mean(value["proportions"]), "total": sum(value["totals"])} )
    except:
        print(f"Issue with country {item}")
for item, value in registers.items(): #value = {"totals:" [12234, 1234, etc.], "proportions": [0.2, 0.45, 0.002 etc.]}
    try:
        register_stats.append({"register": item,
                        "stdev":statistics.stdev(value["proportions"]), 
                       "mean": statistics.mean(value["proportions"]), "total": sum(value["totals"])} )
    except:
        print(f"Issue with register {item}")
for item, value in regions.items(): #value = {"totals:" [12234, 1234, etc.], "proportions": [0.2, 0.45, 0.002 etc.]}
    try:
        region_stats.append({"region": item,
                        "stdev":statistics.stdev(value["proportions"]), 
                       "mean": statistics.mean(value["proportions"]), "total": sum(value["totals"])} )
    except:
        print(f"Issue with region {item}")

country_stats.sort(key=lambda x: x["stdev"], reverse=True)
register_stats.sort(key=lambda x: x["stdev"], reverse=True)
region_stats.sort(key=lambda x: x["stdev"], reverse=True)

with open ("C:/Users/shkunn/Documents/results/differences/tld_country_stdev.txt", "a") as f:
    f.write("Top 50 countries by standard deviation within tlds:\n")
    for d in country_stats[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/differences/tld_register_stdev.txt", "a") as f:
    f.write("Top 50 registers by standard deviation within tlds:\n")
    for d in register_stats[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/differences/tld_region_stdev.txt", "a") as f:
    f.write("Top 50 regions by standard deviation within tlds:\n")
    for d in region_stats[:50]:
       json.dump(d,f)
       f.write("\n\n")


