import json
import statistics

# pull standard deviations of values to show how much different things vary
    #maybe variance of registers within countries? would be interesting to see which registers are spread out evenly
    #at least religion probably has a big standard deviation, description with intent to sell maybe lower 

tlds = {}   #keys are names of tlds, 
registers = {}
regions = {}


with open ("C:/Users/shkunn/Downloads/countries_together_output.txt") as file:
    f = file.read()
    f_json = json.loads(f)
    for country, content in f_json.items():
        tld = content["tld"]        #dictionary of tld: 12345 key-value pairs
        register = content["register"]
        region = content["regional_relevance"]
        total = sum(tld.values())
        
        for item, value in tld.items(): 
            if item in tlds.keys():
                tlds[item]["totals"].append(value)
                tlds[item]["proportions"].append(value / total)
            else:
                tlds[item] = {"totals": [value], "proportions": [value / total]}
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

tld_stats = [] #keys: tlds. values: {standard deviation: 0.00, mean: 0.00, total: 000  }
register_stats = []
region_stats = []
for item, value in tlds.items(): #value = {"totals:" [12234, 1234, etc.], "proportions": [0.2, 0.45, 0.002 etc.]}
    try:
        tld_stats.append({"tld": item,
                        "stdev":statistics.stdev(value["proportions"]), 
                       "mean": statistics.mean(value["proportions"]), "total": sum(value["totals"])} )
    except:
        print(f"Issue with tld {item}")
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

tld_stats.sort(key=lambda x: x["stdev"], reverse=True)
register_stats.sort(key=lambda x: x["stdev"], reverse=True)
region_stats.sort(key=lambda x: x["stdev"], reverse=True)

with open ("C:/Users/shkunn/Documents/results/differences/countries_tld_stdev.txt", "a") as f:
    f.write("Top 50 tlds by standard deviation within countries:\n")
    for d in tld_stats[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/differences/countries_register_stdev.txt", "a") as f:
    f.write("Top 50 registers by standard deviation within countries:\n")
    for d in register_stats[:50]:
       json.dump(d,f)
       f.write("\n\n")

with open ("C:/Users/shkunn/Documents/results/differences/countries_region_stdev.txt", "a") as f:
    f.write("Top 50 regions by standard deviation within countries:\n")
    for d in region_stats[:50]:
       json.dump(d,f)
       f.write("\n\n")

#miten eroaa, jos lasket tämän countries-datalla? 
# entä muilla komboilla? lähtödatana tld, rekisteri tai region/regions?

